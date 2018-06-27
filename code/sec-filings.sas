
options nocenter nodate source;

%let wrds = wrds.wharton.upenn.edu 4016;
options comamid = TCP remote = WRDS;
signon username=reggie09 pw=WtRuP5rT;

libname rwork slibref=work server=wrds;

libname home 'C:\Users\Reginald\Dropbox\Research\0_datasets'; 
libname mydata 'C:\Users\Reginald\Dropbox\Research\Text Analysis of Filings\cossim\data';

data filings;
set home.filings; 
run;
/*15,378,105*/

rsubmit;
proc sql;
create table compustat_ciks as
select distinct cik, gvkey, cusip, tic, fyear, sich
from comp.funda
where not missing(cik)
	and not missing(fyear)
	and not missing(sich)
	and fyear > 1991
	and final='Y'
	and at>0
order by tic, cik, fyear;
quit;
proc download;run;
endrsubmit;
/*192,629*/

/* select 10-K filings from filings which holds all SEC filings */
data filings10k;
set filings;
where formtype IN ("10-K", "10-K/A", "10-K405", "10-K405/A", 
		"10-KSB", "10-KSB/A", "10-KT", "10-KT/A", "10KSB", 
		"10KSB/A", "10KSB40", "10KSB40/A", "10KT405", 
		"10KT405/A");
run;
/*277,324*/

data temp;
set filings10k;
cik2 = put(cik, z10.);
drop cik;
run;

data filings10k;
set temp;
rename cik2=cik;
run;

proc sql;
create table temp as
select a.*, b.*
from compustat_ciks as a,
filings10k as b
where a.cik = b.cik
and a.fyear = year(b.date);
quit;
/*152,788*/

proc sort data=temp out=temp2 nodupkey;
by cik fyear;
run;
/*121,494*/

PROC EXPORT DATA = temp2
            OUTFILE= "C:\Users\Reginald\Dropbox\Research\0_datasets\filings-10k.txt" 
            DBMS=TAB REPLACE;
RUN;
