#! /usr/bin/env bash
# To be run on EC2 instance
# TODO: Create a log file to send versus status reports

# Install python-dev, python-setuptools, emacs
sudo apt-get install python-dev python-setuptools emacs
# Use easy_install for pip
sudo easy_install pip

# Install Amazon Cli
sudo pip install awscli --ignore-installed six

# Configure Amazon Cli

# Download and configure Amazon Python SDK (boto3)
sudo pip install boto3
sudo pip install botocore
	
# Install NFS for EFS mounting
sudo apt-get install nfs-common

# create necessary folders
mkdir efs
mkdir efs/10k
mkdir SAP