# qb-json-next

A python 3 implementation of [qb-json-next](https://github.com/quicbit-js/qb-json-next). Please refer to
that documentation for more detail.

While this is the same logic as the nodejs version that parses at almost 300 MB per second, common
python (CPython 3.7.7) will parse the same files at only 1/100th of that rate (2.5 MB per second).

However, PyPy runs a respectable 100 MB per second, so for fast json scanning in pure python, this 
is the recommended route.

C scanning parses at 800 GB per second on my 2014 macbook pro, so for maximum speed scanning JSON, that would
the way to go, but it isn't as mature or featured as the nodejs version.
 
The reasons for the performance discrepancies have to do with the highly optimized iteration of bytes. Boxing every
byte is relatively very high cost to all the rest of the code that uses integer comparisons and switch
statements in NodeJS. Just the cost of checking on each byte in python is a significant hit even 
when using bytearray.
