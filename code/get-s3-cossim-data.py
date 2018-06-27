#!/usr/bin/env python
import os

WORKING_DATA_DIR = '../data/working'
RESULTS_DATA_DIR = '../data/results'
OUTPUT_FILE = RESULTS_DATA_DIR + '/' + 'cossim.txt'

## Retrieve file list from S3 bucket
def get_s3_files():
    #os_command = "aws s3 ls s3://btcoal/cossim/ | awk '{print $4}' > %s/s3-cossim-files.txt" % DIR
    #os.system(os_command)
    s3_files=[]
    with open('%s/s3-cossim-files.txt' % WORKING_DATA_DIR, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line.find('cossim-') > -1:
                s3_files.append(line)
    print s3_files
    ## Retrieve files from S3 bucket
    for x in s3_files:
        os_command = "aws s3 cp s3://btcoal/cossim/%s %s" % (x, WORKING_DATA_DIR)
        os.system(os_command)

    return s3_files

def combine(s3_files):
    ## add header
    #s3_file_location_on_disk = DIR + '/cossim_s3_files' + '/' + s3_files[0]
    #os_command = "head --lines=+1 %s > %s" % (s3_file_location_on_disk, OUTPUT_FILE)
    header = '\t'.join(['filename_1', 'filename_2', 'file1_words', 'file2_words', 'file1_dwords', 'file2_dwords','cos_sim'])
    os_command = "echo -e '%s' > %s" % (header, OUTPUT_FILE)
    os.system(os_command)

    for x in s3_files:
        s3_file_location_on_disk = WORKING_DATA_DIR + '/' + x
        print s3_file_location_on_disk
        ## skip headers of remaining files
        os_command = "tail --lines=+2 %s >> %s" % (s3_file_location_on_disk, OUTPUT_FILE)
        os.system(os_command)
    return None

def compress():
    os_command = "gzip %s" % OUTPUT_FILE
    os.system(os_command)
    return None

if __name__ == '__main__':
    #s3_files = get_s3_files()
    s3_files = ['cossim-34.212.82.125.txt', 'cossim-34.214.14.2.txt',
                'cossim-34.216.142.245.txt', 'cossim-34.217.104.148.txt',
                'cossim-34.217.147.81.txt', 'cossim-52.32.221.182.txt',
                'cossim-52.34.152.38.txt', 'cossim-52.40.153.47.txt',
                'cossim-52.89.86.180.txt', 'cossim-54.149.155.233.txt',
                'cossim-54.186.42.104.txt', 'cossim-54.191.209.192.txt',
                'cossim-54.191.39.251.txt', 'cossim-54.191.44.53.txt',
                'cossim-54.191.68.67.txt', 'cossim-54.200.178.47.txt',
                'cossim-54.202.153.156.txt', 'cossim-54.244.63.131.txt',
                'cossim-54.245.205.148.txt', 'cossim-54.68.57.67.txt']
    combine(s3_files)
    #compress()
