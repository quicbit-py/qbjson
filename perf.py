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

import jnext
import time


def parse (ps):
  t0 = time.time()

  count = 0
  while 1:
    count += 1
    if count % 1000000 == 0:
      print 'parsed ' + str(count) + ' tokens'
    if not jnext.jnext(ps):
      break

  return (time.time() - t0) * 1000

fname = '../../../dev/json-samples/cache_150mb.json'
# fname = '../../../dev/json-samples/batters_obj.json'
with open(fname, mode='rb') as f:
  buf = f.read()
  print 'read ' + f.name
  ps = jnext.new_ps(buf)
  total_ms = parse(ps)
  print 'parsed ' + str(len(buf)/(1024*1024)) + ' MB in ' + str(total_ms/1000) + ' seconds'


print str(len(buf) / ((total_ms/1000) * 1024 * 1024)) + ' MB/second'

# Test result n 2014 Macbook Pro: 2020-05-16:
#
# read ../../../dev/json-samples/cache_150mb.json
# /Users/dad/dev/py/qb-json-next/bin/python /Users/dad/ghub/py/qb-json-next/perf.py
# parsed 1000000 tokens
# parsed 2000000 tokens
# parsed 3000000 tokens
# parsed 4000000 tokens
# parsed 5000000 tokens
# parsed 6000000 tokens
# parsed 7000000 tokens
# parsed 8000000 tokens
# parsed 9000000 tokens
# parsed 144 MB in 65.6365721226 seconds
# 2.19898019009 MB/second

# NODE JS much faster - same file parsed 5 times shows over 100x speed on nodejs
#
# Test result on 2014 Macbook Pro: 2020-02-15:
#
# /Users/dad/.nvm/versions/node/v8.10.0/bin/node /Users/dad/ghub/qb-json-next/export/perf.js
# read /Users/dad/dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 0.549 seconds
# parsed 144.33352184295654 MB in 0.549 seconds
# parsed 144.33352184295654 MB in 0.565 seconds
# parsed 144.33352184295654 MB in 0.545 seconds
# parsed 144.33352184295654 MB in 0.534 seconds
# 263.19022947293314 MB/second

