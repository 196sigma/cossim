#!/usr/bin/env python
from Section10k import *
import pickle
import time

INPUT_DIR = '/home/reggie/Dropbox/Research/Text Analysis of Filings/docdistance/inputdata'

parsed_db = pickle.load(open("/home/reggie/Dropbox/Research/Text Analysis of Filings/docdistance/inputdata/info/parsed_db", "rb"))

def make_corpus(corpus_description, parsed_db, corpus = None):
    if corpus is None:
        section_corpus = Corpus(corpus_description)
    else:
        section_corpus = corpus
    
    for k in parsed_db.keys():
        v = parsed_db[k]
        filename = INPUT_DIR + '/' + k
        cik = v[0]
        fy = v[4]
        period = v[5]
        xbrl_section = v[7]
            
        section_corpus.add_section10k(Section(filename, cik, fy, period, xbrl_section))
    
    return section_corpus

def get_section_similarity(parsed_sections):
    ## Add header
    header = '\t'.join(['cik1', 'fy1', 'period1', 'cik2', 'fy2', 'period2', 'dist\n'])
    with open('section_similarity.txt', 'w') as outfile:
        outfile.write(header)
    outlines = []
    count = 0
    vals = parsed_sections.values()
    ## Different firms in the same fiscal year
    for sec1 in vals:
        for sec2 in vals:
            cik1 = sec1.cik
            cik2 = sec2.cik
            fy1 = sec1.fy
            fy2 = sec2.fy
            period1 = sec1.period
            period2 = sec2.period
            if cik1 != cik2:
                if fy1 == fy2:
                    section_doc_distance = get_simt(sec1, sec2)
                    outlines.append('\t'.join([cik1, fy1, period1, cik2, fy2, period2, str(section_doc_distance)+'\n']))
                    count += 1
                    if len(outlines) > 1000:
                        #print count
                        with open('section_similarity.txt', 'a') as outfile:
                            outfile.writelines(outlines)
                        outlines = []


    ## The same firm in different fiscal years
    for sec1 in vals:
        for sec2 in vals:
            cik1 = sec1.cik
            cik2 = sec2.cik
            fy1 = sec1.fy
            fy2 = sec2.fy
            period1 = sec1.period
            period2 = sec2.period
            if cik1 == cik2:
                if fy1 != fy2:
                    section_doc_distance = get_simt(sec1, sec2)
                    outlines.append('\t'.join([cik1, fy1, period1, cik2, fy2, period2, str(section_doc_distance)+'\n']))
                    count += 1
                    if len(outlines) > 1000:
                        #print count
                        with open('section_similarity.txt', 'a') as outfile:
                            outfile.writelines(outlines)
                        outlines = []
                        
    with open('section_similarity.txt', 'a') as outfile:
        outfile.writelines(outlines)

    print count
    return count

def get_nobs(parsed_sections):
    count = 0
    vals = parsed_sections.values()
    ## Different firms in the same fiscal year
    for sec1 in vals:
        for sec2 in vals:
            cik1 = sec1.cik
            cik2 = sec2.cik
            fy1 = sec1.fy
            fy2 = sec2.fy
            period1 = sec1.period
            period2 = sec2.period
            if cik1 != cik2:
                if fy1 == fy2: ## Different firms in the same fiscal year
                    count += 1
            else:
                if fy1 != fy2: ## The same firm in different fiscal years
                    count += 1
    return count

if __name__ == '__main__':
    def test(n):
        extime = 0
        ## Sample database of parsed files
        pdb = {}
        for i in range(n):
            k = parsed_db.keys()[i]
            pdb[k] = parsed_db[k]
        ## Generate corpus object from parsed files
        sap_corpus = make_corpus('Significant Accounting Policies Corpus', pdb)    
        pickle.dump(sap_corpus, open('sap_corpus','wb'))

        ## Calculate similarity on 10-K Sections
        parsed_sections = sap_corpus.section_list
        
        start_time = time.time()
        get_section_similarity(parsed_sections)
        extime = time.time() - start_time
        return (get_nobs(parsed_sections), extime)
