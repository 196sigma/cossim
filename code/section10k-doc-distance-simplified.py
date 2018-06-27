#!/usr/bin/env python
## To be run on each EC2 instance

from math import acos, pi, sqrt, log
import os
import sys
import time
import pickle
import string

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




INPUT_DIR = "/home/reggie/Dropbox/Research/Accounting Risk/data"
parsed_db = pickle.load(open(INPUT_DIR + '/parsed_db', 'rb'))

"""
filenames_list = os.listdir(INPUT_DIR+'/SAPTextBlock')
## remove small files
s=0
for f in filenames_list:
    if os.path.getsize(INPUT_DIR+'/SAPTextBlock/'+f) < 1262.55:
        filenames_list.remove(f)
        s+=1
pickle.dump(filenames_list, open('../data/filenames_list','wb'))
"""
filenames_list = pickle.load(open('../data/filenames_list','rb'))
s = len(filenames_list)

def match(file1, file2):
	try:
		cik1 = parsed_db[file1][0]
		cik2 = parsed_db[file2][0]
		fy1 = parsed_db[file1][4]
		fy2 = parsed_db[file2][4]
		if (cik1 != cik2) and (fy1==fy2):
			return True
		elif (cik1 == cik2) and (fy1 != fy2):
			return True
	except:
		return False
	
def get_filedata(filename):
	d={}
	d['cik'] = parsed_db[filename][0]
	d['fy'] = parsed_db[filename][4]
	return d

def test4(outputfilename='cossim.txt', 
		  filestocompare = '/home/reggie/Dropbox/Research/Accounting Risk/data/filestocompare.txt', 
		  output_dir="/home/reggie/Dropbox/Research/Accounting Risk/data", 
		  input_dir="/home/reggie/Dropbox/Research/Accounting Risk/data/SAPTextBlock"):
	
	filestocompare = '/home/reggie/Dropbox/Research/Accounting Risk/data/temp_pairs.txt'

	with open(output_dir+'/' + outputfilename,'w') as outfile:
		outfile.write('file1\tfile2\tcossim\n')
	
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
			if len(docdist) > 100000:
				with open(output_dir+'/' + outputfilename,'a') as outfile:
					for pair, cossim in docdist.items():
						file1_data = getfiledata(file1)
						file2_data = getfiledata(file2)
						outfile.write('\t'.join([pair[0], pair[1], file1_data['cik'], file2_data['cik'], file1_data['fy'], file2_data['fy'], str(cossim)])+'\n')
				docdist = {}

	with open(output_dir+'/' + outputfilename,'a') as outfile:
		for pair, cossim in docdist.items():
			#outfile.write('\t'.join([pair[0], pair[1], str(cossim)])+'\n')
			file1, file2 = pair[0:2]
			file1_data = get_filedata(file1)
			file2_data = get_filedata(file2)
			outfile.write('\t'.join([file1, file2, file1_data['cik'], file2_data['cik'], file1_data['fy'], file2_data['fy'], str(cossim)])+'\n')			
	extime = time.time() - start_time
	
	return extime

    
if __name__ == '__main__':
	print test4()
