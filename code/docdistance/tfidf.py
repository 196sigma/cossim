# tfidf.py
import textmining
from math import log

filename_1 = "inputdata/goog-20091231.txt"
filename_2 = "inputdata/goog-20101231.txt"

doc1 = open(filename_1,'r').readlines()
doc2 = open(filename_2,'r').readlines()
doc1 = ' '.join(doc1).strip()
doc2 = ' '.join(doc2).strip()
doc_set = [doc1, doc2]


## w:   a word token
## d:   a document as a string
def get_tf(w, d):
    tf = 0
    doc_tokens = d.split()
    n_tokens = len(doc_tokens)
    return 1.0*sum([1*(w == token) for token in doc_tokens])/n_tokens

## w:   a word token
## doc_set:   a document set (a list of documents as strings)
def get_idf(w, doc_set):
    n_docs = len(doc_set)
    total_occurences = 0
    for d in doc_set:
        doc_tokens = d.split()
        total_occurences += 1*(w in doc_tokens)
    #print 'N = ',n_docs, 'T = ', total_occurences
    return 1+log(1.0*n_docs/total_occurences, 10)

## w:   a word token
## d_index:
## doc_set: 
def get_tfidf(w, d_index, doc_set):        
    d = doc_set[d_index]
    tf = get_tf(w,d)
    idf = get_idf(w, doc_set)

    ## collect results
    tfidf = {}
    tfidf[w] = tf*idf
    return tfidf

## Get a term-document matrix, optionally weighted by tf-idf
## doc_set: a document set (a list of documents as a string)
def get_tdm(doc_set):
    tdm = textmining.TermDocumentMatrix()
    for d in doc_set:
        tdm.add_doc(d)
    tdm = [line for line in tdm.rows(cutoff=1)]
    return tdm
