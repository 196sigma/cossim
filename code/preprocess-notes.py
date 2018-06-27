#!/usr/bin/env python

## 18 March 2018
## Preprocess 10-K footnotes for COSSIM:
##  - Remove stopwords
##  - lemmatize
##  - lowercase
##  - remove alphanumeric sequences
##  - remove punctuation
## Runs on an EC2 instance

from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import os
import re
DATA_DIR = "/home/ubuntu"
RAW_DATA_DIR = DATA_DIR +'/' + 'NOTES'
OUTPUT_DIR = DATA_DIR + '/' + 'CLEANED'

porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()

notes_files = os.listdir(RAW_DATA_DIR)
for f in notes_files:
    outfilename = f
    out_tokens = []
    out_tokens2 = []
    
    f = open(RAW_DATA_DIR + '/' + f, 'r').read()
    tokens = f.split()
    for x in tokens:
        x = x.lower()
        ## remove numbers
        x = re.sub(r'[0-9]+', ' ', x)
        ## remove punctuation
        x = re.sub(r'[^A-Za-z0-9]+', ' ', x)
        x = x.strip()
        x = x.split()
        out_tokens.extend(x)
        
    for x in out_tokens:
        x = wordnet_lemmatizer.lemmatize(x)
        x = porter_stemmer.stem(x)
        out_tokens2.append(x)
        
    outlines = ' '.join(out_tokens2)
    with open(OUTPUT_DIR + '/' + outfilename, 'w') as outfile:
        outfile.write(outlines)    
