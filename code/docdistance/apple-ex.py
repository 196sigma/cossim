#!/usr/bin/env python
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re

loc = '/home/reggie/Dropbox/Research/Text Analysis of Filings/code/analyze/cossim/code/docdistance'
filename1 = 'apple-example-raw.txt'
raw = open(loc + '/' + filename1, 'r').read()
raw = raw.lower()
tokens = raw.replace('\n', ' ')
tokens = re.sub(r'[0-9]+', ' ', tokens)
tokens = tokens.strip().split()


porter_stemmer = PorterStemmer()
ps = []
for w in tokens:
    try:
        w = porter_stemmer.stem(w)
        ps.append(w)
    except:
        continue

stemmed = ' '.join(ps)
with open(loc + '/apple-example-stemmed.txt', 'w') as outfile:
    outfile.write(stemmed)


sw_removed = stemmed
stops = stopwords.words('english')
stops.append('compani')
stops.append('thi')
sw_removed = [w for w in stemmed.split() if w not in stopwords.words('english')]
sw_removed = ' '.join(sw_removed)
with open(loc + '/apple-example-sw.txt', 'w') as outfile:
    outfile.write(sw_removed)
