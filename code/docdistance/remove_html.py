#/usr/bin/env python
from bs4 import BeautifulSoup, SoupStrainer
import re
import os
#from HTMLParser import HTMLParser

## CREATED: 23 May 2017
## AUTHOR: Reginald Edwards
## MODIFIED:
## DESCRIPTION:

#Searchstrings in regular expressions
tenkend = 'ENDOFTENK'

def remove_html_2(data):
    data = re.sub(r'^M[^a-z]+\n', r'\n', data, flags=re.DOTALL)
    data = re.sub(r'<\/SEC-DOCUMENT>', r'ENDOFTENK', data, flags=re.IGNORECASE | re.DOTALL) #Mark end of 10K
    data = re.sub(r'<\/p>', r'.', data, flags=re.IGNORECASE | re.MULTILINE) #End of sentence for paragraph
    data = re.sub(r'<\/div>', r'.',data, flags=re.IGNORECASE | re.MULTILINE) #End of sentence for paragraph
    data = re.sub(r'<br.{0,2}>', r'.',data, flags=re.IGNORECASE | re.MULTILINE) #End of sentence for break
    data = re.sub(r'<\/tr>', r'.\n', data, flags=re.IGNORECASE | re.MULTILINE) #Break line for end of table rows
    data = re.sub(r'<.*?>', r' ', data, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) #Remove html tags (starts with "<", ends with ">")
    data = re.sub(r'&.{2,6};', r'', data, flags=re.IGNORECASE | re.MULTILINE) #Replace all HTML entities with spaces
    return data

def remove_html(page):
    #Pre-processing the html content by removing extra white space and combining then into one line.
    page = page.strip()  #<=== remove white space at the beginning and end
    page = page.replace('\n', ' ') #<===replace the \n (new line) character with space
    page = page.replace('\r', '') #<===replace the \r (carriage returns -if you're on windows) with space
    page = page.replace('&nbsp;', ' ') #<===replace "&nbsp;" (a special character for space in HTML) with space. 
    page = page.replace('&#160;', ' ') #<===replace "&#160;" (a special character for space in HTML) with space.
    page = page.replace('Table of Contents', '\n')
    while '  ' in page:
        page = page.replace('  ', ' ') #<===remove extra space

    soup = BeautifulSoup(page, "lxml")
    
    #soup.text removes the html tags and only keep the texts
    rawText = soup.text.encode('utf8') #<=== you have to change the encoding the unicodes
    
    rawText += tenkend

    
    #Text Cleanup            
    rawText = re.sub(r'(\'s|\"|\(|\))', '', rawText)    #Remove symbols from words (e.g. ['s] and ["])
    rawText = re.sub(r'[^A-Za-z0-9 .?!]{3,}',' ', rawText)   #Remove string it it consists of 3 or more non-alphanumeric characters
    rawText = re.sub(r'\.([0-9])', r'\1', rawText) #Look for false end of sentences

    #Optional Text Cleanup
    rawText = re.sub(r'\.*\s*\.', r'.', rawText, flags=re.MULTILINE | re.DOTALL) #Remove double end of sentences
    rawText = re.sub(r'  ',r' ', rawText) #Remove double spaces
    rawText = re.sub(r'\n\s+',r'\n', rawText)  #Remove redundant empty lines
    rawText = re.sub(r'\n{3,}',r'\n', rawText) #Remove redundant empty lines
    print len(rawText)
    return rawText

INPUT_DIR = "/home/reggie/Dropbox/Research/Text Analysis of Filings/code/analyze/cossim/code/docdistance/inputdata"
OUTPUT_DIR = "/home/reggie/Dropbox/Research/Text Analysis of Filings/code/analyze/cossim/code/docdistance/cleaned"

for f in os.listdir(INPUT_DIR):
    cleaned = remove_html(open(INPUT_DIR + '/' + f, 'r').read())
    with open(OUTPUT_DIR + '/' + f, 'w') as outfile:
        outfile.write(cleaned)
