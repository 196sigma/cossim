## AUTHOR: Reginald Edwards
## CREATED: 20 March 2018
## MODIFIED: 26 June 2018
## DESCRIPTION: This software calculates cosine similarity between the Notes to 
## the Financial Statements (footnotes, or notes) from firm 10-K filings hosted 
## on the SEC's EDGAR database.

## OVERVIEW
The raw data consists of cleaned footnotes extracted from 10-Ks. As of 20 March 2018, these data are stored in and AWS S3 bucket "s3://btcoal/notes". Different programs are needed to a) download the 10-Ks, b) extract the footnotes, and c) clean the footnotes.

To compute cosine similarity between two sets of footnotes, first generate a list of files to compare. The list of files to compare is based on matching gvkey, sic2, and fiscal year. Specifically, firms that have different GVKEYs and the same SIC2 and the same fiscal year are a match. Use these criteria to generate a list of all pairs of documents between which to compute cossim. 

To distribute computation on EC2:
1.	Split this list into 20 equally-sized chunks. 
2.	Create 20 EC2 instances. 
3.	Send all extracted footnotes files to all 20 EC2 instances. 
4.	Feed in list of pairs to a python script that computes cossim. 
5.	Store cossim values in a text file with file 1 name, file 2 name, and cossim.
6. 	Send filed with cossim values and metadata to S3. (s3://btcoal/cossim as of 03/20/2018.)

## FILE STRUCTURE
/code
- cossim.py
- cossim-ec2-driver.py
- get_filestocompare.py
- get-s3-cossim-data.py

/data
- raw/
  - extracted-10k-notes.txt
- working/
	- filestocompare.txt
	- s3-cossim-files.txt
	- cossim-XXX where XXX is an EC2 instance IP address
- results/
	- cossim.txt
