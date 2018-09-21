%define revcount %(git rev-list HEAD | wc -l)
%define treeish %(git rev-parse --short HEAD)
%define localmods %(git diff-files --exit-code --quiet  || date +.m%%j%%H%%M%%S)

%define srcdir   %{getenv:PWD}

Summary: Redgates Keymaker Service
Name: keymaker
Version: 1.0
Release: %{revcount}.%{treeish}%{localmods}
Distribution: Redgates
Group: System Environment/Daemons
License: Proprietary
Vendor: Redgates
Packager: Karl Redgate <Karl.Redgate@gmail.com>
BuildArch: noarch

%define _topdir %(echo $PWD)/rpm
BuildRoot: %{_topdir}/BUILDROOT

Requires: filesystem
Requires: openssh-server
Requires: nodejs
Requires: nodejs-inherits1
Requires: npm

%description
Tools for the keymaker service

%prep
%build

%install

DIR_ARGS=" -d --mode=755 "
DATA_ARGS=" --mode=644 "
PROG_ARGS=" --mode=755 "

%{__install} $DIR_ARGS $RPM_BUILD_ROOT/usr/share/keymaker/aws/policy
%{__install} $DATA_ARGS %{srcdir}/policy/* $RPM_BUILD_ROOT/usr/share/keymaker/aws/policy

%{__install} $DIR_ARGS $RPM_BUILD_ROOT/usr/share/keymaker/keys
%{__install} --mode=600 %{srcdir}/keys/* $RPM_BUILD_ROOT/usr/share/keymaker/keys

%{__install} $DIR_ARGS $RPM_BUILD_ROOT/usr/libexec/keymaker/setup/
%{__install} $PROG_ARGS %{srcdir}/libexec/keymaker/setup/* $RPM_BUILD_ROOT/usr/libexec/keymaker/setup/

%{__install} $DIR_ARGS $RPM_BUILD_ROOT/usr/bin
%{__install} $PROG_ARGS %{srcdir}/bin/* $RPM_BUILD_ROOT/usr/bin

# add plugin to AWS motd generation service
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/update-motd.d
%{__install} $PROG_ARGS %{srcdir}/etc/update-motd.d/* $RPM_BUILD_ROOT/etc/update-motd.d

%{__install} $DIR_ARGS $RPM_BUILD_ROOT/var/log/keymaker

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,keymaker,keymaker,0755)
%attr(755,root,root,) /etc/update-motd.d/41-keymaker-banner
%attr(755,root,root,) /usr/bin/generate-federated-credentials
%attr(755,root,root,) /usr/bin/generate-assumed-role
/usr/share/keymaker/aws/
/usr/libexec/keymaker/setup/
%attr(644,keymaker,keymaker) /usr/share/keymaker/keys/*.pub
/var/log/keymaker

%pre

getent group keymaker || groupadd keymaker
getent passwd keymaker || useradd keymaker -g keymaker
groupmems --group keymaker --add ec2-user > /dev/null 2>&1 || : ignore error

%post

/usr/libexec/keymaker/setup/create-authorized-users
/usr/libexec/keymaker/setup/install-nodejs-aws-sdk

[ "$1" -gt 1 ] && {
    : Upgrading
}

[ "$1" = 1 ] && {
    : New install
}

: Done

%triggerin -- firstboot
# Disable firstboot any time it gets installed or upgraded
/sbin/chkconfig --level 12345 firstboot off

%changelog

* Thu Apr 30 2015 Redgates <www.redgates.com>
- Initial build

# vim:autoindent expandtab
