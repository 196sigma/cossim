#!/usr/bin/env python
from __future__ import division
from bs4 import BeautifulSoup, SoupStrainer
from HTMLParser import HTMLParser
import os
import time
import pickle
import re

# parse_10K.py
## CREATED: 27 August 2016
## AUTHOR: Reginald Edwards
## MODIFIED:
## DESCRIPTION: Get the footnotes/summary of accounting section of a 10-K filing

DIR = "/home/reggie/Dropbox/Research/Text Analysis of Filings/footnotes/data"
RAW_10K_DIR = DIR + "/raw"
PARSED_HTML_DIR = DIR +  "/parsed-html"
PARSED_NON_HTML_DIR = DIR + "/parsed-non-html"
PARSED_DIR = DIR + "/parsed"

def separate_html(raw_10k_list):
    non_html_list = []
    html_list = []
    for f in raw_10k_list:
        found_html_tag = False
        file_10k_location = RAW_10K_DIR + '/' + f
        with open(file_10k_location, 'r') as text_10k:
            for line in text_10k:
                line = line.lower()
                if line.find('html>') >= 0:
                    html_list.append(f)
                    found_html_tag = True
                    break
        if not found_html_tag:
            non_html_list.append(f)
    html_list = set(html_list)
    non_html_list = set(non_html_list)
    print "%d HTML files" % len(html_list)
    print "%d Non-HTML files" % len(non_html_list)
    pickle.dump(html_list, open(DIR+'/html_list','wb'))
    pickle.dump(non_html_list, open(DIR+'/non_html_list','wb'))
    return None

#separate_html(os.listdir(RAW_10K_DIR))
## Load lists of HTML and NON-HTML files
html_list = pickle.load(open(DIR+'/html_list','rb'))
non_html_list = pickle.load(open(DIR+'/non_html_list','rb'))


def parse_item8(infile):
    f = infile
    parsed = False
    #print f
    file_10k_location = RAW_10K_DIR + '/' + f

    ## remove line breaks
    text_10k = open(file_10k_location, 'r').read()

    ## Remove non-HTML content (e.g. XML)
    html_start = max(text_10k.find('<HTML>'), text_10k.find('<html>'))
    html_end = max(text_10k.find('</HTML>'), text_10k.find('</html>'))
    text_10k = text_10k[(html_start-1):(html_end+8)]
    soup = BeautifulSoup(text_10k, "lxml")

    links ={}
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            links[link.get_text()]=link['href']
            
    item8_link = None
    
    for k in links.keys():
        if 'Item 8' in k:
            item8_link = links[k]
            break
        elif 'item 8' in k:
            item8_link = links[k]
            break
        elif 'Financial Statements' in k:
            item8_link = links[k]
            break            

    ## Search through markup for name associated with Item 8 href
    if item8_link:
        for link in soup.find_all('a'):
            if link.has_attr('name'):
                if link['name'] == item8_link.replace("#",''):
                    print link
                    item8_contents_link = link

                    item8_contents_index = text_10k.find(str(item8_contents_link))
                    
                    if item8_contents_index >= 0:
                        item8_contents = text_10k[item8_contents_index:]

                        ## Remove HTML tables and tags
                        item8_soup = BeautifulSoup(item8_contents)
                        for table_tag in item8_soup.findAll('table'):
                            table_tag.extract()
                        item8_text = item8_soup.text

                        with open(PARSED_HTML_DIR + '/' + f , 'w') as outfile:
                            outfile.write(item8_text.encode('ascii', 'ignore'))
                        parsed = True
    return parsed

def parse_sap(infile):
    f = infile
    parsed = False
    file_10k_location = RAW_10K_DIR + '/' + f
    text_10k = open(file_10k_location, 'r').read()
    ## Remove non-HTML content (e.g. XML)
    html_start = max(text_10k.find('<HTML>'), text_10k.find('<html>'))
    html_end = max(text_10k.find('</HTML>'), text_10k.find('</html>'))
    text_10k = text_10k[(html_start-1):(html_end+8)]
    soup = BeautifulSoup(text_10k, "lxml")
    soup_contents = soup.text

    for div in soup.find_all('div'):
        if "summary of significant accounting polic" in div.get_text().lower():
            contents_index = soup_contents.find(div.get_text())
            
            if contents_index >= 0:
                contents = soup_contents[contents_index:]
                contents = contents.encode('ascii', 'ignore')

                with open(PARSED_HTML_DIR+'/' + f , 'w') as outfile:
                    outfile.write(contents)
                parsed = True
                break
    return parsed

def parse_notes(infile):
    f = infile
    parsed = False
    file_10k_location = RAW_10K_DIR + '/' + f
    text_10k = open(file_10k_location, 'r').read()
    ## Remove non-HTML content (e.g. XML)
    html_start = max(text_10k.find('<HTML>'), text_10k.find('<html>'))
    html_end = max(text_10k.find('</HTML>'), text_10k.find('</html>'))
    text_10k = text_10k[(html_start-1):(html_end+8)]
    soup = BeautifulSoup(text_10k, "lxml")
    soup_contents = soup.text

    for div in soup.find_all('div'):
        if "notes to consoldated financial statements" in div.get_text().lower():
            contents_index = soup_contents.find(div.get_text())        
            if contents_index >= 0:
                contents = soup_contents[contents_index:]
                contents = contents.encode('ascii', 'ignore')

                with open(PARSED_HTML_DIR + '/' + f , 'w') as outfile:
                    outfile.write(contents)
                parsed = True
                break
    return parsed

def parse_item8_div(infile):
    f = infile
    parsed = False
    file_10k_location = RAW_10K_DIR + '/' + f
    text_10k = open(file_10k_location, 'r').read()
    ## Remove non-HTML content (e.g. XML)
    html_start = max(text_10k.find('<HTML>'), text_10k.find('<html>'))
    html_end = max(text_10k.find('</HTML>'), text_10k.find('</html>'))
    text_10k = text_10k[(html_start-1):(html_end+8)]
    soup = BeautifulSoup(text_10k, "lxml")
    soup_contents = soup.text

    for div in soup.find_all('div'):
        if "item 8" in div.get_text().lower():
            contents_index = soup_contents.find(div.get_text())            
            if contents_index >= 0:
                contents = soup_contents[contents_index:]
                contents = contents.encode('ascii', 'ignore')

                with open(PARSED_HTML_DIR+'/' + f , 'w') as outfile:
                    outfile.write(contents)
                parsed = True
                break
    return parsed

def parse_html_regex(infile):
    parsed = False
    
    #print infile
    file_10k_location = RAW_10K_DIR + '/' + infile
    ## remove line breaks
    text_10k = open(file_10k_location, 'r').read()

    ## Remove non-HTML content (e.g. XML)
    html_start = max(text_10k.find('<HTML>'), text_10k.find('<html>'))
    html_end = max(text_10k.find('</HTML>'), text_10k.find('</html>'))
    text_10k = text_10k[(html_start-1):(html_end+8)]

    ## remove html
    soup_10k = BeautifulSoup(text_10k, "lxml")
    contents_10k = soup_10k.text
    contents_10k = contents_10k.encode('ascii', 'ignore')
            
    ## Parse
    target_lines = re.finditer(r'[1-9]\.(.*)SIGNIFICANT(\s*)ACCOUNTING(\s*)POLICIES\s*', contents_10k, re.IGNORECASE) 
    try:
        match_line = target_lines.next()
        section_index = match_line.start(0)
        with open(DIR+'/parsed-temp/'+infile, 'w') as outfile:
            outfile.write(contents_10k[section_index:])
        parsed = True
        print parsed
    except:
        parsed = False
    return parsed

def parse_html(infile):
    if parse_sap(infile):
        return True
    elif parse_notes(infile):
        return True
    elif parse_item8_div(infile):
        return True
    elif parse_item8(infile):
        return True
    elif parse_html_regex(infile):
        return True
    else:
        return False

def parse_non_html(infile):
    parsed = False
    f = ''.join(open(RAW_10K_DIR + '/' + infile,'r').readlines())
    #target_lines = re.findall(r'[1-9](.*)ACCOUNTING(\s+)POLICIES\s+', f, re.IGNORECASE)
    target_lines = re.finditer(r'[1-9](.*)ACCOUNTING(\s+)POLICIES\s+', f, re.IGNORECASE) 
    try:
        match_line = target_lines.next()
        section_index = match_line.start(0)
        with open(PARSED_NON_HTML_DIR+'/'+infile, 'w') as outfile:
            outfile.write(f[section_index:])
        parsed = True
    except:
        parsed = False
    return parsed

    
def parse():
    parsed_html_list = []
    non_parsed_html_list = []
    parsed_non_html_list = []
    non_parsed_non_html_list = []
    
    for infile in html_list:
        parsed = parse_html(infile)
        if parsed:
            parsed_html_list.append(infile)
        else:
            non_parsed_html_list.append(infile)
    parsed_html_list = set(parsed_html_list)
    non_parsed_html_list = set(non_parsed_html_list)
    pickle.dump(parsed_html_list, open(DIR+'/parsed_html_list' , 'wb'))
    pickle.dump(non_parsed_html_list, open(DIR+'/non_parsed_html_list' , 'wb'))
    print "HTML: %d parsed, %d not parsed" % (len(html_list)-len(non_parsed_html_list), len(non_parsed_html_list))
    """
    for infile in non_html_list:
        parsed = parse_non_html(infile)
        if parsed:
            parsed_non_html_list.append(infile)
        else:
            non_parsed_non_html_list.append(infile)
    parsed_non_html_list = set(parsed_non_html_list)
    non_parsed_non_html_list = set(non_parsed_non_html_list)
    pickle.dump(parsed_non_html_list, open(DIR+'/parsed_non_html_list' , 'wb'))
    pickle.dump(non_parsed_non_html_list, open(DIR+'/non_parsed_non_html_list' , 'wb'))
    print "Non-HTML: %d parsed, %d not parsed" % (len(non_html_list)-len(non_parsed_non_html_list), len(non_parsed_non_html_list))
    """

    return None


if __name__ == '__main__':
    parse()
