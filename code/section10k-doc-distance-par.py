#!/usr/bin/env python
## To be run on each EC2 instance

from math import acos, pi, sqrt, log
import os
import sys
import time
import pickle
import string

output_dir ="/home/ubuntu/xbrl"
parsed_db = pickle.load(open(output_dir + '/parsed_db', 'rb'))

## Accepts file locations on disk as input
def get_simf(filename_1, filename_2, verbose=False):
    ## read files
    doc1 = open(filename_1, 'r').readlines()
    doc2 = open(filename_2, 'r').readlines()

    ## make token list (tokenize)
    ## Remove punctuation
    doc1_string = ' '.join(doc1) ## a long string
    out1 = doc1_string.translate(string.maketrans("",""), string.punctuation)
    doc1_tokens = out1.split()
    
    doc2_string = ' '.join(doc2) ## a long string
    out2 = doc2_string.translate(string.maketrans("",""), string.punctuation)
    doc2_tokens = out2.split()

    ## count frequencies
    def get_token_freqs(doc_tokens):    
        token_freqs = {}
        for w in set(doc_tokens):
            token_freqs[w] = 0
        for w in doc_tokens:
            token_freqs[w] += 1
        return token_freqs

    ## get list of common tokens
    tokens = list(set(doc1_tokens) | set(doc2_tokens))

    ## get counts of tokens
    doc1_token_freqs = get_token_freqs(doc1_tokens)
    doc2_token_freqs = get_token_freqs(doc2_tokens)

    ## get counts of tokens in both documents
    occurences = {w:[0,0] for w in tokens}

    for w in doc1_tokens:
        occurences[w][0] += 1
    for w in doc2_tokens:
        occurences[w][1] += 1

    dotprod = sum([freq[0]*freq[1] for freq in occurences.values()])

    doc1_size = sqrt(sum([freq**2 for freq in doc1_token_freqs.values()]))
    doc2_size = sqrt(sum([freq**2 for freq in doc2_token_freqs.values()]))

    cos_sim = acos(dotprod/(1.0*doc1_size*doc2_size))

    file1_lines = len(doc1)
    file2_lines = len(doc2)
    file1_words = len(doc1_tokens)
    file2_words = len(doc2_tokens)
    file1_dwords = len(doc1_token_freqs.keys())
    file2_dwords = len(doc2_token_freqs.keys())
    if verbose:
        print "File %s : %f lines, %f words, %f distinct words" % (filename_1, file1_lines, file1_words, file1_dwords)
        print "File %s : %f lines, %f words, %f distinct words" % (filename_2, file2_lines, file2_words, file2_dwords)
        print "The distance between the documents is: %f (radians)" % cos_sim
    
    return cos_sim
	
def get_filedata(filename):
	d={}
	d['cik'] = parsed_db[filename][0]
	d['fy'] = parsed_db[filename][4]
	return d

def run_ec2(ec2_IP):
	outputfilename='cossim-%s.txt' % ec2_IP
        #print outputfilename
	filestocompare = output_dir + '/pairs-%s.txt' % ec2_IP 
        #print filestocompare
	input_dir="/home/ubuntu/xbrl/SAPTextBlock"

	with open(output_dir+'/' + outputfilename,'w') as outfile:
		outfile.write('\t'.join(['file1', 'file2', 'cik1', 'cik2','fy1','fy2','cossim'])+'\n')
	start_time = time.time()
	
	docdist = {}
	with open(filestocompare,'r') as pairs:
		for line in pairs:
			line = line.strip().split()
			file1, file2 = line[0], line[1]
		
			try:
				docdist[(file1, file2)] = get_simf(input_dir+'/'+file1, input_dir+'/'+file2)
			except:
				docdist[(file1, file2)] = 0

	with open(output_dir+'/' + outputfilename,'a') as outfile:
		for pair, cossim in docdist.items():
			file1, file2 = pair[0], pair[1]
			file1_data = get_filedata(file1)
			file2_data = get_filedata(file2)
			outfile.write('\t'.join([file1, file2, file1_data['cik'], file2_data['cik'], file1_data['fy'], file2_data['fy'], str(cossim)])+'\n')			
	extime = time.time() - start_time
	
	return extime

    
if __name__ == '__main__':
    ec2_IP = sys.argv[1]
    run_ec2(ec2_IP)

    ## Send to S3
    cossim_filename = '/home/ubuntu/xbrl/cossim-%s.txt' % ec2_IP
    os_command = "aws s3 cp %s s3://redwards-xbrl/cossim/" % cossim_filename
    os.system(os_command)
