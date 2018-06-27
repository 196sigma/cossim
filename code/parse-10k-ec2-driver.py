#!/usr/bin/env python
import os
import time
import boto3

PEM_KEY_LOC = '/home/reggie/Dropbox/aws-reg-key-1.pem'
AMI_ID = "ami-8ac460ea"
SEC_GROUP_ID='sg-23ab2245'
N_INSTANCES = 2
DIR = "/home/ubuntu/10k"
RAW_10K_DIR = DIR + "/raw"
PARSED_HTML_DIR = DIR +  "/parsed-html"
PARSED_NON_HTML_DIR = DIR + "/parsed-non-html"
PARSED_DIR = DIR + "/parsed"
_10k_location="/home/reggie/Dropbox/Research/Text Analysis of Filings/cossim/data/10k-files-list.txt"
_10k_location="/home/reggie/Dropbox/Research/Text Analysis of Filings/cossim/code/urls-sample.txt"
_10k_location="/home/reggie/Dropbox/Research/Text Analysis of Filings/cossim/code/urls-sample-big.txt"

## Get instance ID's, IP addresses
def get_ec2_instances():
    ec2 = boto3.resource('ec2')        
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    ec2_instance_list = [i.public_ip_address for i in instances]
    
    return ec2_instance_list

## send list of appropriate 10k files to each instance (split)
def send_10k_helper(start_index, stop_index, ec2_IP):
    ## create file name for sample of 10k to be sent to this EC2 instance
    _10k_sample_filename = "10k-%s.txt" % ec2_IP

    ## Get sample of 10k to send to this EC2 instance
    _10k = open(_10k_location,'r').readlines()
    _10k = _10k[start_index:stop_index]
    with open(_10k_sample_filename,'w') as outfile:
        outfile.writelines(_10k)
        
    ## send 10k file to EC2 instance
    os.system("scp -o StrictHostKeyChecking=no -i ~/.ssh/aws-reg-key-1.pem %s ubuntu@%s:10k" % (_10k_sample_filename, ec2_IP))

    return None

def send_10k(ec2_instance_list=[]):
    n_instances = len(ec2_instance_list)
    _10k = open(_10k_location,'r').readlines()
    n_files = len(_10k)
    sample_size = int(n_files/n_instances)
    print '%d files, %d instances, %d files per instance' % (n_files, n_instances, sample_size)
    i = 0
    while i < (n_instances-1):
        send_10k_helper(i*sample_size, (1+i)*(sample_size), ec2_instance_list[i])
        i += 1
    if i == (n_instances-1):
        send_10k_helper(i*sample_size, n_files, ec2_instance_list[i])
    return None

## run code to parse files on each instance
def run_parse(ec2_instance_list):
    for ec2_IP in ec2_instance_list:
        os_command ="ssh -o StrictHostKeyChecking=no -i ~/.ssh/aws-reg-key-1.pem -f ubuntu@%s \'./10k/parse-10k-ec2.py %s\'" % (ec2_IP, ec2_IP)
        print os_command
        print os.system(os_command)
    return None

if __name__ == '__main__':
	## Spawn EC2 instances
    ec2 = boto3.resource('ec2')
    #ec2.create_instances(ImageId=AMI_ID, InstanceType="t2.micro", SecurityGroupIds=[SEC_GROUP_ID], MinCount=1, MaxCount=N_INSTANCES)
    #time.sleep(60)
    
    ec2_instance_list = get_ec2_instances()
    print ec2_instance_list
    
    ## Mount EFS to each EC2 instance
    ec2_command = "sudo mount -t nfs4 us-west-2b.fs-baee1513.efs.us-west-2.amazonaws.com:/ efs"
    for ec2_IP in ec2_instance_list:
        os_command = "ssh -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
        print os.system(os_command)
        
    send_10k(ec2_instance_list)
    
    ## send parse code
    for ec2_IP in ec2_instance_list:
        os_command = "scp -o StrictHostKeyChecking=no -i ~/.ssh/aws-reg-key-1.pem parse-10k-ec2.py ubuntu@%s:10k" % ec2_IP
        print os.system(os_command)
    
    run_parse(ec2_instance_list)
