from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re

a = """Additionally, changes to noncontrolling interests in the Consolidated Statement of Changes in Equity were $(29) million, $8 million and $(1) million for the years ended December 31, 2011, 2010 and 2009, respectively
The accounts of variable interest entities (VIEs) are included in the Consolidated Financial Statements, if required."""

porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()
out_tokens = []
out_tokens2 = []
tokens = a.split()
for x in tokens:
    x = x.lower()
    x = re.sub(r'[0-9]+', ' ', x)
    x = re.sub(r'[^A-Za-z0-9]+', ' ', x)
    x = x.strip()
    x = x.split()
    out_tokens.extend(x)
    
for x in out_tokens:
    x = wordnet_lemmatizer.lemmatize(x)
    x = porter_stemmer.stem(x)
    out_tokens2.append(x)

u'addit chang to noncontrol interest in the consolid statement of chang in equiti were million million and million for the year end decemb and respect the account of variabl interest entiti vie are includ in the consolid financi statement if requir'
