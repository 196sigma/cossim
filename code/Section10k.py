#!/usr/bin/env python
from __future__ import division
from math import acos, pi, sqrt, log

## Section10k.py
class Section():
    def __init__(self, filename, cik, fy, period, xbrl_section):
        self.filename = filename
        self.cik = cik
        self.fy = fy
        self.period = period
        self.xbrl_section = xbrl_section
        
        ## Convert file contents into one long string
        contents = open(filename,'r').readlines()
        self.contents = ' '.join([w.strip() for w in contents])
        

    ## Tokenize contents string
    def get_tokens(self):
        ## Remove punctuation
        contents = self.contents
        contents = contents.replace('.','')
        contents = contents.replace(',','')
        contents = contents.replace('?','')
        contents = contents.replace('!','')
        contents = contents.replace(';','')
        contents = contents.replace(':','')
        contents = contents.replace('\"','')
        contents = contents.replace('(','')
        contents = contents.replace(')','')
        contents = contents.replace('[','')
        contents = contents.replace(']','')
        tokens = contents.split()
        return tokens
    
    def get_token_freqs(self):
        tokens = self.get_tokens()
        unique_tokens = set(tokens)
        freqs = {w:0 for w in unique_tokens}
        for w in tokens:
            freqs[w] += 1
        return freqs
    
    def remove_stopwords(self):
        pass

class Corpus():
    def __init__(self, description):
        self.description = description
        self.section_list = {}
        self.length = len(self.section_list)

    def contains(self, section10k):
        new_section10k_id = '-'.join([section10k.cik, section10k.fy, section10k.period, section10k.xbrl_section])
        return new_section10k_id in self.section_list
    
    def add_section10k(self, section10k):
        if not self.contains(section10k):
            section10k_id = '-'.join([section10k.cik, section10k.fy, section10k.period, section10k.xbrl_section])
            self.section_list[section10k_id] = section10k
            self.length += 1
        else:
            print '10-K Section already in corpus. Moving on...'
        return None
    
    def get_section10k(self, document_id):
        return self.section_list[document_id]
    
    def get_sections(self):
        return self.section_list
    

            

## Takes two Section objects as input
def get_simt(section1, section2, verbose=False):
    doc1_tokens = section1.get_tokens()
    doc2_tokens = section2.get_tokens()
    doc1_token_freqs = section1.get_token_freqs()
    doc2_token_freqs = section2.get_token_freqs()
    
    ## get list of common tokens
    tokens = list(set(doc1_tokens) | set(doc2_tokens))

    ## get counts of tokens in both documents
    occurences = {w:[0,0] for w in tokens}

    for w in doc1_tokens:
        occurences[w][0] += 1
    for w in doc2_tokens:
        occurences[w][1] += 1

    dotprod = sum([freq[0]*freq[1] for freq in occurences.values()])

    doc1_size = sqrt(sum([freq**2 for freq in doc1_token_freqs.values()]))
    doc2_size = sqrt(sum([freq**2 for freq in doc2_token_freqs.values()]))

    try:
        cos_sim = acos(dotprod/(doc1_size*doc2_size))
    except:
        cos_sim = 0

    file1_words = len(doc1_tokens)
    file2_words = len(doc2_tokens)
    file1_dwords = len(doc1_token_freqs.keys())
    file2_dwords = len(doc2_token_freqs.keys())
    if verbose:
        print "File %s : %f words, %f distinct words" % (section1.cik+' '+section1.fy, file1_words, file1_dwords)
        print "File %s : %f words, %f distinct words" % (section2.cik+' '+section2.fy, file2_words, file2_dwords)
        print "The distance between the documents is: %f (radians)" % cos_sim
    
    return cos_sim
