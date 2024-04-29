#!/bin/bash

    region=${REGION:-"ap-northeast-1"} && \
    aws_url="https://${region}.console.aws.amazon.com/ec2/home?region=${region}#KeyPairs:" && \
    echo "Please find your SSH key pair name from below URL" && \
    echo "Press enter to open ${aws_url}" && \
    read enter && \
    open "$aws_url" && \
    default_name=masafumi.kashiwagi && \
    echo -n "Enter your ssh key name [$default_name]: " && \
    read ssh_key && \
    ssh_key=${ssh_key:-$default_name} && \
    timestamp=$(date +%s) && \
    
    # Retrieve my public IP address
    my_ip=$(curl -s https://checkip.amazonaws.com) && \
        
    # Retrieve the username
    user_name=$(aws --region ${region} sts get-caller-identity --query 'Arn' --output text | rev | cut -d/ -f1 | rev | sed -e 's/@.*//') && \
        
    # Set the instance name based on the username
    instance_name="${user_name}-kvm-${timestamp}" && \
        
    # Create a security group
    subnet_id=${SUBNET_ID:-"subnet-099904a6ad96204d6"} && \
    vpc_id=$(aws --region ${region} ec2 describe-subnets --subnet-ids $subnet_id --query 'Subnets[*].VpcId' --output text) && \
    if [[ -n $SG_CREATE ]] && [[ "${SG_CREATE,,}" != "false" ]]; then
        sg_id=$(aws --region ${region} ec2 create-security-group --group-name "$instance_name" --description "Security group for SSH and RDP access" --query 'GroupId' --vpc-id "$vpc_id" --output text)
        # Allow SSH access (port 22)
        aws --region ${region} ec2 authorize-security-group-ingress --group-id $sg_id --protocol tcp --port 22 --cidr ${my_ip}/32
        # Allow RDP access (port 3389)
        aws --region ${region} ec2 authorize-security-group-ingress --group-id $sg_id --protocol tcp --port 3389 --cidr ${my_ip}/32
    elif [[ -n $SG_ID ]]; then
        sg_id=$SG_ID
    else
        sg_id=$(aws ec2 describe-security-groups --filters Name=vpc-id,Values=${vpc_id} Name=group-name,Values='default' --query 'SecurityGroups[0].GroupId' --output text)
    fi && \
        
    # Specify the AMI ID and instance type
    ami_id=${AMI_ID:-"ami-0adb3635eb20f395b"} && \
    
    # Deploy instance from Launch Template
    instance_id=$(aws --region ${region} ec2 run-instances --image-id $ami_id --instance-type c5.metal --security-group-ids $sg_id --subnet-id $subnet_id --key-name "$ssh_key" --count 1 --query 'Instances[0].InstanceId' --output text --user-data '#!/bin/bash
echo "ubuntu:Datadog/4u" | sudo chpasswd
') && \

    # Set Name tag of instance
    aws --region ${region} ec2 create-tags --resources $instance_id --tags Key=Name,Value=$instance_name && \

    # Output the instance name and Public IP
    echo "---------------------------------" && \
    echo "Instance name: ${instance_name}" && \
    echo "RDP Password: Datadog/4u" && \
    aws_url="https://${region}.console.aws.amazon.com/ec2/home?region=${region}#InstanceDetails:instanceId=${instance_id}" && \
    echo "" && \
    echo "Press enter to open instance page" && \
    read enter && \
    open "$aws_url"
