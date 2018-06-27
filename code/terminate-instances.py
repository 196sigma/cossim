#!/usr/bin/env python
import boto3
import time

if __name__ == '__main__':
	ec2 = boto3.resource('ec2')        
	instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	ec2_instance_list = [i.instance_id for i in instances]
	
	i=0
	for instance in ec2_instance_list:
		i+=1
		print i, instance
	
	ec2.instances.filter(InstanceIds=ec2_instance_list).terminate()
