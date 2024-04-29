#!/bin/bash

aws_url="https://ap-northeast-1.console.aws.amazon.com/ec2/home?region=ap-northeast-1#KeyPairs:" && \
echo "Please find your SSH key pair name from below URL" && \
echo "Press enter to open ${aws_url}" && \
read enter && \
open "$aws_url" && \
default_name=masafumi.kashiwagi && \
echo -n "Enter your ssh key name [$default_name]: " && \
read ssh_key && \
export ssh_key=${ssh_key:-$default_name} && \

# Retrieve my public IP address
my_ip=$(curl -s https://checkip.amazonaws.com) && \

# Retrieve the username
user_name=$(aws sts get-caller-identity --query 'Arn' --output text | rev | cut -d/ -f1 | rev | sed -e 's/@.*//') && \

# Set the instance name based on the username
instance_name="${user_name}-kvm-$(date +%s)" && \

# Create a security group
sg_id=$(aws ec2 create-security-group --group-name $instance_name --description "Security group for SSH and RDP access" --query 'GroupId' --output text) && \

# Allow SSH access (port 22)
aws ec2 authorize-security-group-ingress --group-id $sg_id --protocol tcp --port 22 --cidr ${my_ip}/32 && \

# Allow RDP access (port 3389)
aws ec2 authorize-security-group-ingress --group-id $sg_id --protocol tcp --port 3389 --cidr ${my_ip}/32 && \

# Specify the AMI ID and instance type
ami_id=ami-0adb3635eb20f395b && \

# Deploy instance from Launch Template
instance_id=$(aws ec2 run-instances --image-id $ami_id --instance-type c5.metal --security-group-ids $sg_id --subnet-id subnet-17b4f661 --key-name "$ssh_key" --count 1 --query 'Instances[0].InstanceId' --output text --user-data '#!/bin/bash
echo "ubuntu:Datadog/4u" | sudo chpasswd
')

# Set Name tag of instance
aws ec2 create-tags --resources $instance_id --tags Key=Name,Value=$instance_name && \

# Output the instance name and Public IP
echo "---------------------------------" && \
echo "Instance name: ${instance_name}" && \
echo "ssh ubuntu@$(aws ec2 describe-instances --instance-ids ${instance_id} --query 'Reservations[*].Instances[*].PublicIpAddress' --output text)" && \
echo "RDP Password: Datadog/4u" && \
aws_url="https://ap-northeast-1.console.aws.amazon.com/ec2/home?region=ap-northeast-1#InstanceDetails:instanceId=${instance_id}" && \
echo "Press enter to open instance page${aws_url}" && \
read enter && \
open "$aws_url"

