
PWD := $(shell pwd)
PACKAGE = keymaker

default: rpm

rpm:
	rm -rf rpm
	mkdir -p rpm/BUILD rpm/RPMS rpm/BUILDROOT
	rpmbuild --quiet -bb --buildroot=$(PWD)/rpm/BUILDROOT $(PACKAGE).spec

clean:
	$(RM) -rf $(CLEANS)
	$(RM) -rf rpm exports
