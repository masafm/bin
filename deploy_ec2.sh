#!/usr/bin/env zsh
set -e

region=${REGION:-"ap-northeast-1"}
aws --region $region ec2 describe-key-pairs --query 'KeyPairs[*].KeyName' --output text | tr '\t' '\n' | sort -f
echo ""
default_name=masafumi.kashiwagi
echo "Please find your SSH key pair name from above list"
echo -n "Enter your ssh key name [$default_name]: "
read ssh_key
ssh_key=${ssh_key:-$default_name}
timestamp=$(date +%s)

# Retrieve my public IP address
my_ip=$(curl -s https://checkip.amazonaws.com)

# Retrieve the username
user_name=$(aws --region ${region} sts get-caller-identity --query 'Arn' --output text | rev | cut -d/ -f1 | rev | sed -e 's/@.*//')
        
# Set the instance name based on the username
instance_name="${user_name}-kvm-${timestamp}"

# Create a security group
subnet_id=${SUBNET_ID:-"subnet-099904a6ad96204d6"}
vpc_id=$(aws --region ${region} ec2 describe-subnets --subnet-ids $subnet_id --query 'Subnets[*].VpcId' --output text)
SG_CREATE=$(echo $SG_CREATE | tr '[:upper:]' '[:lower:]')
if [[ -n $SG_CREATE ]] && [[ "${SG_CREATE}" != "false" ]]; then
    sg_id=$(aws --region ${region} ec2 create-security-group --group-name "$instance_name" --description "Security group for SSH and RDP access" --query 'GroupId' --vpc-id "$vpc_id" --output text)
    # Allow SSH access (port 22)
    aws --region ${region} ec2 authorize-security-group-ingress --group-id $sg_id --protocol tcp --port 22 --cidr ${my_ip}/32
    # Allow RDP access (port 3389)
    aws --region ${region} ec2 authorize-security-group-ingress --group-id $sg_id --protocol tcp --port 3389 --cidr ${my_ip}/32
    # Allow ICMP
    aws --region ${region} ec2 authorize-security-group-ingress --group-id $sg_id --protocol icmp --port -1 --cidr ${my_ip}/32
elif [[ -n $SG_ID ]]; then
    sg_id=$SG_ID
else
    sg_id=$(aws ec2 describe-security-groups --filters Name=vpc-id,Values=${vpc_id} Name=group-name,Values='default' --query 'SecurityGroups[0].GroupId' --output text)
fi

# Specify the AMI ID and instance type
ami_id=${AMI_ID:-"ami-0adb3635eb20f395b"}

# Deploy instance from AMI
instance_id=$(aws --region ${region} ec2 run-instances --image-id $ami_id --instance-type c5.metal --security-group-ids $sg_id --subnet-id $subnet_id --key-name "$ssh_key" --count 1 --query 'Instances[0].InstanceId' --output text --user-data '#!/bin/bash
echo "ubuntu:Datadog/4u" | sudo chpasswd
')

# Set Name tag of instance
aws --region ${region} ec2 create-tags --resources $instance_id --tags Key=Name,Value=$instance_name

# Output the instance name
echo "---------------------------------"
echo "Instance name: ${instance_name}"
sleep 1
echo "Public IP: $(aws ec2 describe-instances --instance-ids "${instance_id}" --query 'Reservations[*].Instances[*].PublicIpAddress' --output text)"
echo "Private IP: $(aws ec2 describe-instances --instance-ids "${instance_id}" --query 'Reservations[*].Instances[*].PrivateIpAddress' --output text)"
echo "RDP Password: Datadog/4u"
sleep 1
aws_url="https://${region}.console.aws.amazon.com/ec2/home?region=${region}#InstanceDetails:instanceId=${instance_id}"
echo $aws_url
open $aws_url

# Comment for avoiding unknown error
