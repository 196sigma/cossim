#/usr/bin/env python
from __future__ import division
from bs4 import BeautifulSoup, SoupStrainer
import re
import os
import nltk
SAP_FILES_DIR = "/media/reggie/607049A4704981B0/xbrl/SAP/sap_corpus_01"
OUTPUT_FILES_DIR = "/home/reggie/Dropbox/Research/0_cossim/data/working"

## TODO: cache bigrams to disk so the analysis can be run on the whole corpus
## without reading all the bigrams into a Python dictionary object in one pass

bigrams_list = {}

doc_set = os.listdir(SAP_FILES_DIR)

for d in doc_set[:1]:
    doc = open(SAP_FILES_DIR + '/' + d, 'r').read()
    doc = doc.split()

    bigrams_iter = nltk.bigrams(doc)

    for b in bigrams_iter:
        if b in bigrams_list:
            bigrams_list[b] += 1
        else:
            bigrams_list[b] = 1

bigrams_list_trimmed = {}
for b in bigrams_list:
    if bigrams_list[b] > 2:
        bigrams_list_trimmed[b] = bigrams_list[b]

with open(OUTPUT_FILES_DIR + '/' + 'bigrams.txt', 'w') as outfile:
    outfile.writelines([k[0] + '\t' + k[1] + '\t' + str(bigrams_list_trimmed[k]) + '\n' for k in bigrams_list_trimmed.keys()])
    
