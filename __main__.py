"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import ec2, s3

env_name = pulumi.get_stack().lower()

# Create an AWS EC2 Key Pair
key_pair = ec2.KeyPair('webserver', public_key='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCiot+o0R5Gsd4+9VtufmYgVQkmNJ060rQrx8IYH8gNscIsSuZg2moYsylfwYZoAJidMjNWUIk87i5e1NEszDaxPsrItaRJcu81jyxHSYI4FiqO/ikzGwM15oc7ryhin55ZNOv6P8oENYcE8a2wqHZDQ9V/BgAAt/u/zMjlAmmmJ9uxLyxX5CVk4xdkEF9J6jfjAnh8nHDCvHyJxxe60oDdOJsYiORk+BgnO102v/mjV9kdcMypz+umO+PoBIeWz4kDozgEJpSX7ZDfxLMYm8ZzBkrgum+qofhCYn1EH9Yo0W7kVp8tT6Q5zhCjKEKf7n40w516t68KZLXl4jVlvEJj0/svhj2evUBNaq9HFHsJRKSzceWKdZj696oxouNMBDlTCmDtqiyIbmw7PBbSsWUgt3qbA1oPBsxaTzKAGjehjZcnq5c8Qv8s8rkIO9nITaVPw3w9rjCMQPovqmNnmhk6RQb8zEi9prb1Suic1lviiwH1axhWN5z2f9BVScrddi5HaxthcRJOD1P/sUeqVxw5Ouc6WWFttJrqHCiF9A8fDjGLXmvoDj7Glo6kmx7vfEBD6urrA1A+Q4MgHE911OYzmcuJgpqzDUiJC11cIgXl6oOeaI5yaVzxj9+ybKQDtlLkKLfyFH83gARA9N6XCUdcHoe48NU/1VUfWZQWaq+mkQ==')

# Create an AWS Security Group
sg = ec2.SecurityGroup('webserver-sg', name="webserver-sg", description="Security Group for webserver")

# Create an AWS Security Group Rule to allow SSH inbound access
allow_ssh = ec2.SecurityGroupRule("Allow-SSH", type='ingress', from_port=22, to_port=22, protocol='tcp', cidr_blocks=['0.0.0.0/0'], security_group_id=sg.id)

# Create an AWS Security Group Rule to allow HTTP inbound access
allow_http = ec2.SecurityGroupRule("Allow-HTTP", type='ingress', from_port=80, to_port=80, protocol='tcp', cidr_blocks=['0.0.0.0/0'], security_group_id=sg.id)

# Create an AWS Security Group Rule to allow HTTPS inbound access
allow_https = ec2.SecurityGroupRule("Allow-HTTPS", type='ingress', from_port=443, to_port=443, protocol='tcp', cidr_blocks=['0.0.0.0/0'], security_group_id=sg.id)

# Create an AWS Security Group Rule to allow all outbound access
allow_all = ec2.SecurityGroupRule("Allow-All", type='egress', from_port=0, to_port=0, protocol='-1', cidr_blocks=['0.0.0.0/0'], security_group_id=sg.id)

instance_names = ["webserver-1", "webserver-2", "webserver-3"]
output_public_ip = []

for instance_name in instance_names:
    ec2_instance = ec2.Instance(
        env_name + '-' + instance_name,
        ami='ami-0c7217cdde317cfec',
        instance_type='t2.micro',
        key_name=key_pair.key_name,
        vpc_security_group_ids=[sg.id],
        tags={
            "Name": instance_name
            })
    output_public_ip.append(ec2_instance.public_ip)

pulumi.export('public_ip', output_public_ip)
# pulumi.export('instance_url', pulumi.Output.concat('http://', ec2_instance.public_ip, '/'))