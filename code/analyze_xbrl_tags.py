#!/usr/bin/env python

## Reginald Edwards
## 23 January 2018 
## Get XBRL tags related to SAP. This will help in parsing the XBRL files to get
## this section.

import os
import xml.etree.ElementTree as ET
import pickle

## location of unzipped XBRL 10-K files
XML_FILES_DIR = "/media/reggie/607049A4704981B0/xbrl/xml-files-unzipped"
WORKING_DATA_DIR = "/home/reggie/Dropbox/Research/0_extractsap/data/working"

xml_files = os.listdir(XML_FILES_DIR)

elemList = {}

for xml_file in xml_files:
    xmlTree = ET.parse(XML_FILES_DIR + '/' + xml_file)

    for elem in xmlTree.iter():
        if elem.tag.find('AccountingPolicies') > -1:
            sap_tag = elem.tag
            sap_tag = sap_tag.split('}')[-1]
            if sap_tag in elemList:
                elemList[sap_tag] += 1
            else:
                elemList[sap_tag] = 1

with open(WORKING_DATA_DIR + '/' + 'sap_tags.txt', "w") as outfile:
    outfile.writelines([k + '\t' + str(elemList[k]) + '\n' for k in elemList.keys()])
