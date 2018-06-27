#!/usr/bin/env python
from __future__ import division
import os
import sys
import time
import pickle
#import string
def set_filings_db2():
    filings_db = {}
    with open("/home/reggie/Dropbox/Research/0_datasets/filings-10k.txt", "r") as infile:
        for line in infile:
            line = line.strip().split('\t')
            cik = line[0]
            coname = line[1]
            url = line[2]
            filingdate = line[3]
            formtype = line[4]
            accno = url.split('/')[-1]
            filings_db[accno] = (cik,coname,filingdate)
    pickle.dump(filings_db, open('../data/filings_db','wb'))
    return None

def set_filings_db():
    filings_db = {}
    with open("/home/reggie/Dropbox/Research/0_datasets/extracted-10k-notes.txt", "r") as infile:
        for line in infile:
            line = line.strip().split('\t')
            cik = line[5]
            gvkey = line[11]
            filingdate = line[3]
            formtype = line[4]
            accno = url.split('/')[-1]
            filings_db[accno] = (cik,coname,filingdate)
    pickle.dump(filings_db, open('../data/filings_db','wb'))
    return None

## Construct database of parsed files
parsed_db = {}
parsed_files = open("/home/reg/Dropbox/Research/0_datasets/extracted-10k-notes.txt","r").readlines()
parsed_files = [x.strip() for x in parsed_files]
parsed_files = parsed_files[1:] ## skip header
for l in parsed_files:
    l = l.split(",")
    cik = l[5]
    gvkey = l[11]
    fyear = l[6]
    fname = l[0]
    sic2 = l[21]
    parsed_db[fname] = (cik, gvkey, fyear, sic2)
    
def set_parsed_db(parsed_files_list, parsed_files_location=""):
    parsed_db = {}
    #parsed_files_list = os.listdir(parsed_files_location)
    for f in parsed_files_list:
        entries = f.split('-')
        cik = entries[0]
        fy = entries[1]
        parsed_db[f] = (cik, fy)
    return parsed_db

#parsed_db = set_parsed_db([line.strip() for line in open('parsed-files.txt', 'r')])
#pickle.dump(parsed_db, open('../data/parsed_db', 'wb'))
#parsed_db = pickle.load(open('../data/filings_db', 'rb'))
def match(file1, file2):
    try:
        cik1 = parsed_db[file1][0]
        cik2 = parsed_db[file2][0]
        fy1 = parsed_db[file1][1]
        fy2 = parsed_db[file2][1]
        if (cik1 != cik2) and (fy1==fy2):
            return True
        elif (cik1 == cik2) and (fy1 != fy2):
            return True
    except:
        return False

def match_gvkey(file1, file2):
    try:
        gvkey1 = parsed_db[file1][1]
        gvkey2 = parsed_db[file2][1]
        fy1 = parsed_db[file1][2]
        fy2 = parsed_db[file2][2]
        sic1 = parsed_db[file1][3]
        sic2 = parsed_db[file2][3]
        if (gvkey1 != gvkey2) and (fy1==fy2) and (sic1 == sic2):
            return True
        elif (gvkey1 == gvkey2) and (fy1 != fy2):
            return True
    except:
        return False

def get_filestocompare(outputfilename='/home/reg/Dropbox/Research/0_cossim/data/working/filestocompare.txt'):
    ## write header
    with open(outputfilename, 'w') as outfile:
        outfile.write('\t'.join(['file1','file2'])+'\n')

    filestocompare = {}
    start_time = time.time()
    parsed_files = parsed_db.keys()
    matches = 0
    for file1 in parsed_files:
        for file2 in parsed_files:
            if match_gvkey(file1, file2) and ((file2, file1) not in filestocompare):
                try:
                    filestocompare[(file1, file2)] = 1
                    matches += 1
                    if matches%100000==0:
                        print time.time()-start_time, matches, ' matches'
                except:
                    continue
    print time.time()-start_time, len(filestocompare)
    with open(outputfilename, 'a') as outfile:
        outfile.writelines(['\t'.join(pair)+'\n' for pair in filestocompare])
    
    return None

outputfilename='/home/reg/Dropbox/Research/0_cossim/data/working/filestocompare.txt'
## write header
with open(outputfilename, 'w') as outfile:
    outfile.write('\t'.join(['file1','file2'])+'\n')

filestocompare = {}
start_time = time.time()
parsed_files = parsed_db.keys()
matches = 0
for file1 in parsed_files:
    for file2 in parsed_files:
        if match_gvkey(file1, file2) and ((file2, file1) not in filestocompare):
            try:
                filestocompare[(file1, file2)] = 1
                matches += 1
                if matches%100000==0:
                    print time.time()-start_time, matches, ' matches'
            except:
                continue
print time.time()-start_time, len(filestocompare)
with open(outputfilename, 'a') as outfile:
    outfile.writelines(['\t'.join(pair)+'\n' for pair in filestocompare])
"""
if __name__ == '__main__':
    get_filestocompare()
"""
