#!/usr/bin/env python
from __future__ import division
import os
import sys
import time
import pickle
#import string

parsed_db = pickle.load(open('/home/reggie/Dropbox/Research/Accounting Risk/data/2009_2016/parsed_db','rb'))

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

def get_filestocompare(outputfilename='/home/reggie/Dropbox/Research/Accounting Risk/data/2009_2016/filestocompare2.txt'):
	#filestocompare = []
	filestocompare = {}
	start_time = time.time()
	parsed_files = parsed_db.keys()
	for file1 in parsed_files:
		for file2 in parsed_files:
			if match(file1, file2) and ((file2, file1) not in filestocompare):
				try:
					filestocompare[(file1, file2)] = 1
				except:
					continue
	with open(outputfilename, 'w') as outfile:
		outfile.writelines(['\t'.join(pair)+'\n' for pair in filestocompare])
	print time.time()-start_time, len(filestocompare)
	
	return None

def foo():
	filestocompare = []
	x=0
	start_time = time.time()
	with open('/home/reggie/Dropbox/Research/Accounting Risk/data/2009_2016/filestocompare.txt','r') as infile:
		for pair in infile:
			x+=1
			if x%10000==0:
				print time.time()-start_time, x
			pair = pair.strip().split()
			pair = sorted(pair)
			if pair not in filestocompare:
				filestocompare.append(pair)
	with open('/home/reggie/Dropbox/Research/Accounting Risk/data/2009_2016/filestocompare3.txt', 'w') as outfile:
		outfile.writelines(['\t'.join(pair)+'\n' for pair in filestocompare])
if __name__ == '__main__':
	get_filestocompare()
	#foo()
