This policy is attached to the role that is associated
with the EC2 instance providing the keymaker service.
Saved here for reference.

The account number needs to change to a new account number
when we change to a new account.

The way this works is the policy document is installed in
an IAM policy.  The IAM policy is then attached to an IAM
role.  The role is used allow actions to be taken by some
software without checking in AWS keys.  The role is attached
to an EC2 instance and is used by the AWS APIs automatically
as the credentials to make requests.

There is one twist.  The AWS CLI doc points out that there is
also a "iam-instance-profile" that is really the thing that is
attached to an EC2 instance.  The instance profile is created
automatically if you create the role from the AWS console.
However, if you create the role using the AWS CLI, you must
also create the instance profile.  Read this page for more
details.

[IAM Roles for EC2]( http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html )

<!-- vim: set autoindent expandtab sw=4 syntax=markdown: -->
