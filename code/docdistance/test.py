from Section10k import *
import pickle

parsed_db = pickle.load(open("/home/reggie/Dropbox/Research/Text Analysis of Filings/xbrl/data/SignificantAccountingPoliciesTextBlock/parsed_db", "rb"))
pdb = {}
for i in range(20):
    k = parsed_db.keys()[i]
    pdb[k] = parsed_db[k]

INPUT_DIR = '/home/reggie/Dropbox/Research/Text Analysis of Filings/xbrl/data/SignificantAccountingPoliciesTextBlock'
corpus_description = 'Significant Accounting Policies Corpus'
sap_corpus = Corpus(corpus_description)

for k in pdb.keys():
    v = pdb[k]
    filename = INPUT_DIR + '/' + k
    cik = v[0]
    fy = v[4]
    period = v[5]
    xbrl_section = 'SignificantAccountingPolicies'
    
    sap_section = Section(filename, cik, fy, period, xbrl_section)
    sap_corpus.add_section10k(sap_section)
    


#doc1 = Section('t8.shakespeare.txt', '0000123456', '2015', '12312015', 'SignificantAccountingPolicies')
#doc2 = Section('t3.lewis.txt', '0000123456', '2015', '12312015', 'SignificantAccountingPolicies')
#corpus1 = Corpus('project gutenberg corpus')
#corpus1.add_section10k(doc1)
#corpus1.add_section10k(doc2)

pickle.dump(sap_corpus, open('corpus_SigAccPol','wb'))
