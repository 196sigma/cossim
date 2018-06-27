#/usr/bin/env python
from __future__ import division
from bs4 import BeautifulSoup, SoupStrainer
from HTMLParser import HTMLParser
import os
import time
import pickle
import re
import sys

# get-item1.py
## CREATED: 22 May 2017
## AUTHOR: Reginald Edwards
## MODIFIED:
## DESCRIPTION: 

DIR = "/home/reggie/Dropbox/Research/Text Analysis of Filings/footnotes/data"
RAW_10K_DIR = DIR + "/raw"
PARSED_HTML_DIR = DIR +  "/parsed-html"
PARSED_NON_HTML_DIR = DIR + "/parsed-non-html"
PARSED_DIR = DIR + "/parsed"
input_path = htmlSubPath+file_name
output_path = txtSubPath+file_name.replace(".htm",".txt")


input_file = open(input_path,'rb')
page = input_file.read()  #<===Read the HTML file into Python


#Pre-processing the html content by removing extra white space and combining then into one line.
page = page.strip()  #<=== remove white space at the beginning and end
page = page.replace('\n', ' ') #<===replace the \n (new line) character with space
page = page.replace('\r', '') #<===replace the \r (carriage returns -if you're on windows) with space
page = page.replace('&nbsp;', ' ') #<===replace "&nbsp;" (a special character for space in HTML) with space. 
page = page.replace('&#160;', ' ') #<===replace "&#160;" (a special character for space in HTML) with space.
while '  ' in page:
    page = page.replace('  ', ' ') #<===remove extra space

#Using regular expression to extract texts that match a pattern
    
#Define pattern for regular expression.
    #The following patterns find ITEM 1 and ITEM 1A as diplayed as subtitles
    #(.+?) represents everything between the two subtitles
#If you want to extract something else, here is what you should change

#Define a list of potential patterns to find ITEM 1 and ITEM 1A as subtitles   
regexs = ('bold;\">\s*Item 1\.(.+?)bold;\">\s*Item 1A\.',   #<===pattern 1: with an attribute bold before the item subtitle
          'b>\s*Item 1\.(.+?)b>\s*Item 1A\.',               #<===pattern 2: with a tag <b> before the item subtitle
          'Item 1\.\s*<\/b>(.+?)Item 1A\.\s*<\/b>',         #<===pattern 3: with a tag <\b> after the item subtitle          
          'Item 1\.\s*Business\.\s*<\/b(.+?)Item 1A\.\s*Risk Factors\.\s*<\/b') #<===pattern 4: with a tag <\b> after the item+description subtitle 

#Now we try to see if a match can be found...
for regex in regexs:
    match = re.search(regex, page, flags=re.IGNORECASE)  #<===search for the pattern in HTML using re.search from the re package. Ignore cases.

    #If a match exist....
    if match:
        #Now we have the extracted content still in an HTML format
        #We now turn it into a beautiful soup object
        #so that we can remove the html tags and only keep the texts
        
        soup = BeautifulSoup(match.group(1), "html.parser") #<=== match.group(1) returns the texts inside the parentheses (.*?) 
        

        #soup.text removes the html tags and only keep the texts
        rawText = soup.text.encode('utf8') #<=== you have to change the encoding the unicodes

       
        #remove space at the beginning and end and the subtitle "business" at the beginning
        #^ matches the beginning of the text
        outText = re.sub("^business\s*","",rawText.strip(),flags=re.IGNORECASE)
        
        output_file = open(output_path, "w")
        output_file.write(outText)  
        output_file.close()
        
        break  #<=== if a match is found, we break the for loop. Otherwise the for loop continues
