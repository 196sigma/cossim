# sec-filings.py
_10K_FILES_LOC = "/home/reggie/Dropbox/Research/0_datasets/filings-10k.txt"
URLS_FILES_LOC = "/home/reggie/Dropbox/Research/0_datasets/urls.txt"
with open(_10K_FILES_LOC, 'r') as infile:
    with open(URLS_FILES_LOC, 'w') as outfile:
        for line in infile:
            line = line.strip().split('\t')
            url = line[8]
            outfile.write('http://www.sec.gov/Archives/'+url+'\n')
        
