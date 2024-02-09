"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
from pulumi_aws import ec2

env_name = pulumi.get_stack().lower()

with open('ssh-pub-key/id_rsa.pub', 'r') as pub_key_file:
    public_key = pub_key_file.read()

with open('scripts/install_nginx_webserver.sh', 'r') as user_data_file:
    user_data = user_data_file.read()

# Create an AWS EC2 Key Pair
key_pair = ec2.KeyPair('webserver', public_key=public_key)

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

instance_names = ["webserver-1"]
output_public_ip = []

ubuntu_ami = ec2.get_ami(
    most_recent=True,
    owners=["099720109477"],
    filters=[
        ec2.GetAmiFilterArgs(
            name="name",
            values=["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"],
        )
    ]
)

for instance_name in instance_names:
    ec2_instance = ec2.Instance(
        env_name + '-' + instance_name,
        ami=ubuntu_ami.id,
        instance_type='t2.micro',
        key_name=key_pair.key_name,
        vpc_security_group_ids=[sg.id],
        user_data=user_data,
        tags={
            "Name": env_name + '-' + instance_name
            })
    output_public_ip.append(ec2_instance.public_ip)

pulumi.export('public_ip', output_public_ip)

for public_ip in output_public_ip:
    pulumi.export('instance_url', pulumi.Output.concat('http://', public_ip, '/'))
