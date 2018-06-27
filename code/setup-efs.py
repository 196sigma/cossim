#!/usr/bin/env python

import boto3
import os

PEM_KEY_LOC = '/home/reggie/Dropbox/aws/aws-key.pem'

def get_ec2_instances():
    ec2 = boto3.resource('ec2')        
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    ec2_instance_list = [i.public_ip_address for i in instances]
    return ec2_instance_list

ec2_instance_list = get_ec2_instances()

## Run mount command
ec2_command = "sudo mount -t nfs4 -o nfsvers=4.1, hard, timeo=600, retrans=2 %s.us-west-2.amazonaws.com:/ efs" % FS_ID
for ec2_IP in ec2_instance_list:
    os_command = "ssh -o UserKnownHostsFile=~/Dropbox/aws/aws_khosts -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
    print os.system(os_command)

## Change owner of mount dir
ec2_command = "sudo chown ubuntu efs"
for ec2_IP in ec2_instance_list:
    os_command = "ssh -o UserKnownHostsFile=~/Dropbox/aws/aws_khosts -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
    os.system(os_command)
