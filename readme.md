# qbjson.jnext()

A python 3 implementation of [qb-json-next](https://github.com/quicbit-js/qb-json-next). Please refer to
that documentation for more detail.

CPython, the most commonly used python interpreter available at python.org, is substantially slower 
than other interpreters for byte scanning. Peformance tests for parsing with jnext a large 
json file (144 MB) on a Mid-2014 Macbook Pro are:

    CPython 3.7.7:      2.9 MB/second
    PyPy 3.7.1:       142.8 MB/second
    NodeJS 8.10.0:    263.2 MB/second (using qb-json-next)
    C:                800   MB/second
    
While the python code is the same logic as the nodejs code common, the NodeJS version parses at 90 times
the rate of CPython and 1.8 times the rate of PyPy.

Interestingly, the PyPy theoretical parsing limit of 1,024 MB per second is substantially higher 
than NodeJS (see below), so there could be substantial room for further improvement.

The C version is bare-bones with minimum featues, but uses some branching parallelization of read to achieve performance -
code available at [quicbit-c/qb-json-next](https://github.com/quicbit-c/qb-json-next)

The reasons for the large performance discrepancies of CPython have to do with autoboxing of every
individual result. The performance advantages of using primative bytes and ints and 
switch statements dissapear when every result is auto-boxed. In short, CPython doesn't let programmers 
operate directly on individual primatives such as bytes read in a file.
... and although there are many libraries that help with aggregate operations on bytes such as numpy, ripping 
JSON into tokens for any type of flexible handling doesn't appear to be implemented.

# How Optimal Are These Implementations?

When trying to achieve optimal performance, it's good practice to establish 
a baseline of the theoretical limit. Ascertaining that limit in these cases is simple and does not
require the use of profilers... in fact, profilers interfere with these measurements. 

To establish a theoretical limit, we pose the hypothesis that it isn't possible in Python to 
parse UTF-8 any faster than with a loop like so:

    i = 0
    lenb = len(buf)
    while i < lenb:
      c = buf[i]
      if c == 0:
        raise Exception('oops') # should not happen - this "== 0" check is a stand-in as fastest-possible logic
      i += 1

... where "buf" is a python bytes array.

This code is in perf_max.py (details of results are in that file as well). 
Theoretical limits for CPython 3.7.7 and PyPy 3.7.1 on a
Mid-2014 Macbook Pro running on a 144 MB file cached in memory come out to be:

    CPython:      8 MB/second
    NodeJS:     493 MB/second   (similar test)
    PyPy:     1,024 MB/second
    C:        2,010 MB/second

NodeJS stat is from [quicbit-js/qb-json-next/export/perf_max.js](https://github.com/quicbit-js/qb-json-next/blob/master/export/perf_max.js)

C stat is from [quicbit-c/qb-json-next/test/perf-max.c](https://github.com/quicbit-c/qb-json-next/blob/master/test/perf-max.c)

Based on this, it 