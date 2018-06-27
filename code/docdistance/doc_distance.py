# doc_distance.py
from math import acos, pi, sqrt, log


filename_1 = "inputdata/goog-20111231.txt"
filename_2 = "inputdata/aapl-20130928.txt"

## w:   a word token
## d:   a document as a string
def get_tf(w, d):
    tf = 0
    doc_tokens = d.split()
    n_tokens = len(doc_tokens)
    return 1.0*sum([1*(w == token) for token in doc_tokens])/n_tokens

## w:   a word token
## doc_set:   a document set
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

## Uses TF-IDF weighting prior to cosine similarity computation
def get_sim2(filename_1, filename_2):

    ## read files
    doc1_tokens = open(filename_1, 'r').read()
    doc2_tokens = open(filename_2, 'r').read()

    ## make token list (tokenize)
    doc1_tokens = doc1_tokens.replace('.', ' ')
    doc1_tokens = doc1_tokens.replace('\n', ' ')
    doc1_tokens = doc1_tokens.replace('\'', ' ')
    doc1_tokens = doc1_tokens.lower()
    doc1_tokens = doc1_tokens.split()

    doc2_tokens = doc2_tokens.replace('.',' ')
    doc2_tokens = doc2_tokens.replace('\n', ' ')
    doc2_tokens = doc2_tokens.replace('\'',' ')
    doc2_tokens = doc2_tokens.lower()
    doc2_tokens = doc2_tokens.split()

    ## get counts of tokens weighted by TF-IDF
    doc1_token_freqs = {}
    doc2_token_freqs = {}
    doc_set = [' '.join(doc1_tokens), ' '.join(doc2_tokens)]
    for w in set(doc1_tokens):
        doc1_token_freqs.update(get_tfidf(w, 0, doc_set))
    for w in set(doc2_tokens):
        doc2_token_freqs.update(get_tfidf(w, 1, doc_set))

    ## get list of common tokens
    tokens = list(set(doc1_tokens) | set(doc2_tokens))
    ## get counts of tokens in both documents
    occurences = {w:[0,0] for w in tokens}

    for w in set(doc1_tokens):
        occurences[w][0] = doc1_token_freqs[w]
    for w in set(doc2_tokens):
        occurences[w][1] = doc2_token_freqs[w]

    dotprod = sum([freq[0]*freq[1] for freq in occurences.values()])

    doc1_size = sqrt(sum([freq**2 for freq in doc1_token_freqs.values()]))
    doc2_size = sqrt(sum([freq**2 for freq in doc2_token_freqs.values()]))

    cos_sim = acos(dotprod/(1.0*doc1_size*doc2_size))

    file1_words = len(doc1_tokens)
    file2_words = len(doc2_tokens)
    file1_dwords = len(doc1_token_freqs.keys())
    file2_dwords = len(doc2_token_freqs.keys())
    print "File %s : %f words, %f distinct words" % (filename_1, file1_words, file1_dwords)
    print "File %s : %f words, %f distinct words" % (filename_2, file2_words, file2_dwords)
    print "The distance between the documents is: %f (radians)" % cos_sim
    
    return (filename_1, filename_2, file1_words, file2_words, file1_dwords, file2_dwords, cos_sim)

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
    filename_2 = filename_1.split('/')[-2]
    return (filename_1, filename_2, file1_words, file2_words, file1_dwords, file2_dwords, cos_sim)

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
        cos_sim = acos(dotprod/(1.0*doc1_size*doc2_size))
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

c = get_sim2(filename_1, filename_2)
#get_sim2(filename_2, filename_3)
#get_sim2(filename_1, filename_3)
#get_sim2(filename_5, filename_8)
