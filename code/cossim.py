#!/usr/bin/env python
## To be run on each EC2 instance

from math import acos, pi, sqrt, log
import os
import sys
import time
import string

OUTPUT_DIR ="/home/ubuntu"
OUTPUT_DIR = ""

## Accepts file locations on disk as input
def get_simf(filename_1, filename_2, verbose=False):
    ## read files
    doc1 = open(filename_1, 'r').readlines()
    doc2 = open(filename_2, 'r').readlines()

    ## make token list (tokenize)
    doc1_tokens = ' '.join(doc1)
    doc1_tokens = doc1_tokens.replace('.',' ')
    #doc1_tokens = doc1_tokens.replace('\'',' ')
    doc1_tokens = doc1_tokens.split()

    doc2_tokens = ' '.join(doc2)
    doc2_tokens = doc2_tokens.replace('.',' ')
    #doc2_tokens = doc2_tokens.replace('\'',' ')
    doc2_tokens = doc2_tokens.split()

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
    filename_1 = filename_1.split('/')[-1]
    filename_2 = filename_2.split('/')[-1]
    return (filename_1, filename_2, file1_words, file2_words, file1_dwords, file2_dwords, cos_sim)

def run_ec2(ec2_IP):
	outputfilename='cossim-%s.txt' % ec2_IP
        print outputfilename
	filestocompare = 'pairs-%s.txt' % ec2_IP 
        print filestocompare
	INPUT_DIR="/home/ubuntu/CLEANED"

	with open(outputfilename,'w') as outfile:
		outfile.write('\t'.join(['filename_1', 'filename_2', 'file1_words','file2_words', 'file1_dwords', 'file2_dwords', 'cos_sim'])+'\n')
	start_time = time.time()
	
	docdist = {}
	with open(filestocompare,'r') as pairs:
                pairs.next()    ## skip header
		for line in pairs:
			line = line.strip().split()
			filename_1, filename_2 = line[0], line[1]
			try:
				docdist[(filename_1, filename_2)] = get_simf(INPUT_DIR+'/'+filename_1,
                                                                             INPUT_DIR+'/'+filename_2)
			except:
				docdist[(filename_1, filename_2)] = (filename_1,filename_2,
                                                                     -1, -1, -1, -1, -1)

	with open(outputfilename,'a') as outfile:
		for pair, cossim in docdist.items():
			filename_1, filename_2 = cossim[0], cossim[1]
                        file1_words, file2_words = cossim[2], cossim[3]
                        file1_dwords, file2_dwords = cossim[4], cossim[5]
                        cos_sim = cossim[6]
                        #print filename_1, filename_2, file1_words, file2_words, file1_dwords, file2_dwords, cos_sim
			outfile.write('\t'.join([filename_1, filename_2, str(file1_words),
                            str(file2_words), str(file1_dwords),
                            str(file2_dwords), str(cos_sim)])+'\n')
	extime = time.time() - start_time
	
	return extime

    
if __name__ == '__main__':
    ec2_IP = sys.argv[1]
    run_ec2(ec2_IP)

    ## Send to S3
    cossim_filename = 'cossim-%s.txt' % ec2_IP
    os_command = "aws s3 cp %s s3://btcoal/cossim/" % cossim_filename
    os.system(os_command)
