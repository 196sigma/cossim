#!/usr/bin/env bash

## To be run on local machine from top project directory as ./code/sample/get-filings.sh

## TDF file with 10k urls and metadata
# file="/home/reggie/Dropbox/Research/Accounting Risk/code/sample/filings-10k-short.txt"
file="filings-10k-short.txt"

## get url portion
awk -F"\t" 'NR!=1{print $3}' $file > urls.txt

## add top-level domain
awk '{print "http://www.sec.gov/Archives/"$0}' urls.txt > urls-2.txt

## Download 
cat urls-2.txt | xargs -n 1 -P 4 wget -q