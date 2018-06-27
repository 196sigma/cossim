#!/usr/bin/env python
import os
import boto3
import time

AMI_ID = "ami-5345582a"
SEC_GROUP_ID='sg-f9d54281'
N_INSTANCES = 20
PEM_KEY_LOC = '/home/reg/Dropbox/aws/aws-key.pem'

DIR = "/home/ubuntu"
PARSED_DIR = DIR + "/" + "CLEANED"
WORKING_DATA_DIR = "/home/reg/Dropbox/Research/0_cossim/data/working"

## Get instance ID's, IP addresses
def get_ec2_instances():
    ec2 = boto3.resource('ec2')        
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    ec2_instance_list = [i.public_ip_address for i in instances]
    return ec2_instance_list

## send list of appropriate 10k files to each instance (split)
def send_pairs_helper(start_index, stop_index, ec2_IP, pairs_file_location):
    ## create file name for sample of 10k to be sent to this EC2 instance
    pairs_sample_filename = WORKING_DATA_DIR + '/' + "pairs-%s.txt" % ec2_IP

    ## Get sample of send to this EC2 instance
    pairs = open(pairs_file_location,'r').readlines()
    pairs = pairs[start_index:stop_index]
    with open(pairs_sample_filename,'w') as outfile:
        outfile.writelines(pairs)
        
    ## send 10k file to EC2 instance
    os.system("scp -o StrictHostKeyChecking=no -i %s %s ubuntu@%s:" % (PEM_KEY_LOC, pairs_sample_filename, ec2_IP))

    return None

def send_pairs(ec2_instance_list, pairs_file_location):
    n_instances = len(ec2_instance_list)
    pairs = open(pairs_file_location,'r').readlines()
    n_files = len(pairs)
    sample_size = int(n_files/n_instances)
    print '%d files, %d instances, %d files per instance' % (n_files, n_instances, sample_size)
    i = 0
    while i < (n_instances-1):
        send_pairs_helper(i*sample_size, (1+i)*(sample_size), ec2_instance_list[i], pairs_file_location)
        i += 1
    if i == (n_instances-1):
        send_pairs_helper(i*sample_size, n_files, ec2_instance_list[i], pairs_file_location)
    return None

def copy_s3_data(ec2_instance_list):
    ## send data: cleaned footnotes extracted from 10-Ks
    for ec2_IP in ec2_instance_list:
        ec2_command = "aws s3 cp s3://btcoal/portstem-notes.tar.gz ."
        os_command = "ssh -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
        print os_command, os.system(os_command)

def extract(ec2_instance_list):
    for ec2_IP in ec2_instance_list:
        ec2_command = "tar -xzf portstem-notes.tar.gz"
        os_command = "ssh -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
        print os_command, os.system(os_command)

## run code to parse files on each instance
def send_code(ec2_instance_list):
    for ec2_IP in ec2_instance_list:
        os_command = "scp -o StrictHostKeyChecking=no -i %s cossim.py ubuntu@%s:" % (PEM_KEY_LOC, ec2_IP)
        print os_command, os.system(os_command)
    return None

def run_code(ec2_instance_list):
    for ec2_IP in ec2_instance_list:
        os_command ="ssh -o StrictHostKeyChecking=no -i %s -f ubuntu@%s \'./cossim.py %s\'" % (PEM_KEY_LOC, ec2_IP, ec2_IP)
        print os_command, os.system(os_command)
    return None
        
if __name__ == '__main__':
    ## Spawn EC2 instances
    ec2 = boto3.resource('ec2')
    print "Creating instances"
    ec2.create_instances(ImageId=AMI_ID, InstanceType="t2.medium",
        SecurityGroupIds=[SEC_GROUP_ID], MinCount=1, MaxCount=N_INSTANCES)

    time.sleep(180)  # Should be enough time to wait for all instances to get up and running

    ec2_instance_list = get_ec2_instances()
    for ec2_IP in ec2_instance_list:
        print ec2_IP
    print "restarting instances"
    ## Run maintenance
    for ec2_IP in ec2_instance_list:
        ec2_command = 'sudo reboot'
        os_command = "ssh -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
        print os_command, os.system(os_command)
    time.sleep(120)
    copy_s3_data(ec2_instance_list)
    time.sleep(60)
    extract(ec2_instance_list)
    
    send_pairs(ec2_instance_list, "/home/reg/Dropbox/Research/0_cossim/data/working/filestocompare.txt")
    #ec2_IP = ec2_instance_list[0]
    #os_command = "scp -o StrictHostKeyChecking=no -i %s pairs-%s.txt ubuntu@%s:" % (PEM_KEY_LOC, ec2_IP, ec2_IP)
    #print os_command, os.system(os_command)    

    send_code(ec2_instance_list)

    #run_code(ec2_instance_list)
    
