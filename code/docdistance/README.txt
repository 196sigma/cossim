####################################################################################################
#   Calculating Cosine Similarity between 10-K Sections
####################################################################################################

parsed_db is a Python dictionary representing a database of parsed XBRL XML files. 
    
    parse_db[filename.txt] = (cik, adsh, name, form, fy, period, sub_url, xbrl_section_tag)
    
PROGRAM STRUCTURE
- doc_distance.py: contains functions for computing cosine similarity between segments of text
- Section10k.py: contains classes for processing of xbrl section text
- section10k-doc-distance:
    - Dependencies: doc_distance.py, Section10k.py


DIRECTORY STRUCTURE
/inputdata
    - /info: Contains metadata about section .txt files 
    - *.txt: extracted XBRL sections; ready for analysis
