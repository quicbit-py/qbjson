#!/usr/bin/python

# Software License Agreement (ISC License)
#
# Copyright (c) 2020, Matthew Voss
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Test the theoretical limit of python interpreters for reading bytes one-by-one from a file.
# Full file is loaded into memory and iterated over with simple "== 0" check.

import jnext
import time

def parse (buf):
  t0 = time.time()

  i = 0
  lenb = len(buf)
  while i < lenb:
    c = buf[i]
    # perform the minimal amount of work on each byte returned
    if c == 0:
      raise Exception('oops')
    i += 1

  return time.time() - t0

path = '../../../dev/json-samples/cache_150mb.json'
# path = '../../../dev/json-samples/cache_1mb.json'
# path = '../../../dev/json-samples/batters_obj.json'
iter = 1
with open(path, mode='rb') as f:
  buf = f.read()
  print('read', f.name)
  total_seconds = 0
  for i in range(iter):
    total_seconds += parse(buf)

  total_mb = (iter * len(buf)) / (1024 * 1024)
  print('parsed', total_mb, 'MB in', total_seconds, 'seconds')

print(total_mb / total_seconds, 'MB/second')

# CPython 3.7.7
#
# /Users/dad/dev/py/qbjson/bin/python /Users/dad/ghub/py/qbjson/perf_max.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 18.061487197875977 seconds
# 7.991231301259074 MB/second

# PyPy 3.7.1
#
# dads-MBP:qbjson dad$ pypy3 perf_max.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 0.14096283912658691 seconds
# 1023.9118532036852 MB/second

# NodeJS 8.10.0
#
# (results from https://github.com/quicbit-js/qb-json-next/blob/master/export/perf_max.js)
#
# /Users/dad/.nvm/versions/node/v8.10.0/bin/node /Users/dad/ghub/qb-json-next/export/perf_max.js
# read /Users/dad/dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 0.328 seconds
# parsed 144.33352184295654 MB in 0.28 seconds
# parsed 144.33352184295654 MB in 0.279 seconds
# parsed 144.33352184295654 MB in 0.296 seconds
# parsed 144.33352184295654 MB in 0.28 seconds
# 493.27929543047344 MB/second
