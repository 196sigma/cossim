## 12 October 2016
## Apple Notes, Significant Accounting Policies (Revenue Recognition) for 2009 and 2011
aapl2009 = ' '.join(open("aapl-rev-rec-2009.txt", 'r').readlines())
aapl2011 = ' '.join(open("aapl-rev-rec-2011.txt", 'r').readlines())

## word count
aapl2009_tokens = aapl2009.split()
aapl2009_word_count = len(aapl2009_tokens)

aapl2011_tokens = aapl2011.split()
aapl2011_word_count = len(aapl2011_tokens)
