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
    # if count % 1000000 == 0:
    #   print('parsed', count, 'tokens')
    if not jnext.jnext(ps):
      break

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
    ps = jnext.new_ps(buf)
    total_seconds += parse(ps)

  total_mb = (iter * len(buf)) / (1024 * 1024)
  print('parsed', total_mb, 'MB in', total_seconds, 'seconds')

print(total_mb / total_seconds, 'MB/second')

# All tests run on Mid-2014 Macbook Pro (2.2 GHz Intel Core i7, 16 GB 1600 MHz DDR3)
#


# CPython 3.7.7 (with skip_str function): slowest
#
# dads-MBP:qbjson dad$ python3 perf.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 57.78302001953125 seconds
# 2.4978535527248376 MB/second
# dads-MBP:qbjson dad$


# CPython 3.7.7 (embedded skip_str logic): a small ~3 percent improvement over skip_str() function call
#
# dads-MBP:qbjson dad$ python3 perf.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 55.90728712081909 seconds
# 2.581658479171828 MB/second


# PyPy 3.7.1 (with skip_str function): 38 times faster than CPython
#
# dads-MBP:qbjson dad$ pypy3 perf.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 1.4544610977172852 seconds
# 99.23505143553298 MB/second

# PyPy 3.7.1 (embedded skip_str logic): a 40% improvement over skip_str() version and 55 times faster than CPython
# dads-MBP:qbjson dad$ pypy3 perf.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 1.0107951164245605 seconds
# 142.79206487809412 MB/second

# NodeJS 8.10.0 (5 passes): 102x faster than CPython (see https://github.com/quicbit-js/qb-json-next/)
#
# /Users/dad/.nvm/versions/node/v8.10.0/bin/node /Users/dad/ghub/qb-json-next/export/perf.js
# read /Users/dad/dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 0.549 seconds
# parsed 144.33352184295654 MB in 0.549 seconds
# parsed 144.33352184295654 MB in 0.565 seconds
# parsed 144.33352184295654 MB in 0.545 seconds
# parsed 144.33352184295654 MB in 0.534 seconds
# 263.19022947293314 MB/second

#############################
# PROFILES
#############################

# CPython 3.7.7 (with skip_str function)
#
# dads-MBP:qbjson dad$ python3 -m cProfile perf.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 62.46955704689026 seconds
# 2.310461745944803 MB/second
#          29540265 function calls (29540259 primitive calls) in 62.557 seconds
#
#    Ordered by: standard name
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1009(_handle_fromlist)
#         ...
#         1    0.000    0.000    0.000    0.000 jnext.py:125(pos_map)
#    117594    0.129    0.000    0.147    0.000 jnext.py:148(skip_bytes)
#  10054456   19.382    0.000   19.382    0.000 jnext.py:168(skip_str)
#         1    0.000    0.000    0.001    0.001 jnext.py:19(<module>)
#         3    0.000    0.000    0.000    0.000 jnext.py:200(skip_dec)
#   9330241   38.723    0.000   59.086    0.000 jnext.py:222(jnext)
#         1    0.000    0.000    0.000    0.000 jnext.py:346(end_src)
#         1    0.000    0.000    0.000    0.000 jnext.py:413(ParseState)
#         1    0.000    0.000    0.000    0.000 jnext.py:414(__init__)
#         1    0.000    0.000    0.000    0.000 jnext.py:439(new_ps)
#         1    0.000    0.000   62.557   62.557 perf.py:19(<module>)
#         1    3.384    3.384   62.470   62.470 perf.py:23(parse)
#        10    0.000    0.000    0.000    0.000 {built-in method _imp.acquire_lock}
#         1    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
#         1    0.000    0.000    0.000    0.000 {built-in method _imp.exec_dynamic}
#         2    0.000    0.000    0.000    0.000 {built-in method _imp.is_builtin}
#         2    0.000    0.000    0.000    0.000 {built-in method _imp.is_frozen}
#        10    0.000    0.000    0.000    0.000 {built-in method _imp.release_lock}
#         4    0.000    0.000    0.000    0.000 {built-in method _thread.allocate_lock}
#         4    0.000    0.000    0.000    0.000 {built-in method _thread.get_ident}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
#         2    0.000    0.000    0.000    0.000 {built-in method builtins.any}
#         1    0.003    0.003    0.003    0.003 {built-in method builtins.compile}
#       2/1    0.000    0.000   62.557   62.557 {built-in method builtins.exec}
#        12    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
#        11    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.id}
#         6    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.iter}
#   5136364    0.391    0.000    0.391    0.000 {built-in method builtins.len}
#        12    0.000    0.000    0.000    0.000 {built-in method builtins.print}
#         2    0.000    0.000    0.000    0.000 {built-in method from_bytes}
#         1    0.000    0.000    0.000    0.000 {built-in method io.open}
#         1    0.000    0.000    0.000    0.000 {built-in method marshal.dumps}
#         4    0.000    0.000    0.000    0.000 {built-in method posix.fspath}
#         2    0.000    0.000    0.000    0.000 {built-in method posix.getcwd}
#         1    0.000    0.000    0.000    0.000 {built-in method posix.open}
#         1    0.000    0.000    0.000    0.000 {built-in method posix.replace}
#        10    0.000    0.000    0.000    0.000 {built-in method posix.stat}
#         2    0.000    0.000    0.000    0.000 {built-in method time.time}
#   2450585    0.213    0.000    0.213    0.000 {method 'append' of 'list' objects}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
#         3    0.000    0.000    0.000    0.000 {method 'endswith' of 'str' objects}
#         4    0.000    0.000    0.000    0.000 {method 'extend' of 'bytearray' objects}
#         1    0.000    0.000    0.000    0.000 {method 'format' of 'str' objects}
#         4    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
#        24    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
#   2450585    0.247    0.000    0.247    0.000 {method 'pop' of 'list' objects}
#         1    0.082    0.082    0.082    0.082 {method 'read' of '_io.BufferedReader' objects}
#         2    0.000    0.000    0.000    0.000 {method 'read' of '_io.FileIO' objects}
#        14    0.000    0.000    0.000    0.000 {method 'rpartition' of 'str' objects}
#        46    0.000    0.000    0.000    0.000 {method 'rstrip' of 'str' objects}
#         3    0.000    0.000    0.000    0.000 {method 'to_bytes' of 'int' objects}
#         1    0.000    0.000    0.000    0.000 {method 'write' of '_io.FileIO' objects}

# CPython 3.7.7 (embedded skip_str logic)
# dads-MBP:qbjson dad$ python3 -m cProfile perf.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 59.12739086151123 seconds
# 2.441060221666401 MB/second
#          19485549 function calls (19485548 primitive calls) in 59.203 seconds
#
#    Ordered by: standard name
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:103(release)
#         ...
#         1    0.000    0.000    0.000    0.000 jnext.py:125(pos_map)
#    117594    0.126    0.000    0.143    0.000 jnext.py:148(skip_bytes)
#         1    0.000    0.000    0.000    0.000 jnext.py:19(<module>)
#         3    0.000    0.000    0.000    0.000 jnext.py:198(skip_dec)
#   9330241   55.419    0.000   56.348    0.000 jnext.py:220(jnext)
#         1    0.000    0.000    0.000    0.000 jnext.py:362(end_src)
#         1    0.000    0.000    0.000    0.000 jnext.py:429(ParseState)
#         1    0.000    0.000    0.000    0.000 jnext.py:430(__init__)
#         1    0.000    0.000    0.000    0.000 jnext.py:455(new_ps)
#         1    0.000    0.000   59.203   59.203 perf.py:19(<module>)
#         1    2.779    2.779   59.127   59.127 perf.py:23(parse)
#         1    0.000    0.000    0.000    0.000 {built-in method _imp._fix_co_filename}
#         5    0.000    0.000    0.000    0.000 {built-in method _imp.acquire_lock}
#         1    0.000    0.000    0.000    0.000 {built-in method _imp.is_builtin}
#         1    0.000    0.000    0.000    0.000 {built-in method _imp.is_frozen}
#         5    0.000    0.000    0.000    0.000 {built-in method _imp.release_lock}
#         2    0.000    0.000    0.000    0.000 {built-in method _thread.allocate_lock}
#         2    0.000    0.000    0.000    0.000 {built-in method _thread.get_ident}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.any}
#       2/1    0.000    0.000   59.203   59.203 {built-in method builtins.exec}
#         6    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
#         3    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
#         2    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.iter}
#   5136362    0.358    0.000    0.358    0.000 {built-in method builtins.len}
#         3    0.000    0.000    0.000    0.000 {built-in method builtins.print}
#         3    0.000    0.000    0.000    0.000 {built-in method from_bytes}
#         1    0.000    0.000    0.000    0.000 {built-in method io.open}
#         1    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
#         3    0.000    0.000    0.000    0.000 {built-in method posix.fspath}
#         1    0.000    0.000    0.000    0.000 {built-in method posix.getcwd}
#         3    0.000    0.000    0.000    0.000 {built-in method posix.stat}
#         2    0.000    0.000    0.000    0.000 {built-in method time.time}
#   2450585    0.204    0.000    0.204    0.000 {method 'append' of 'list' objects}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
#         1    0.000    0.000    0.000    0.000 {method 'endswith' of 'str' objects}
#         2    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
#         8    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
#   2450585    0.242    0.000    0.242    0.000 {method 'pop' of 'list' objects}
#         1    0.075    0.075    0.075    0.075 {method 'read' of '_io.BufferedReader' objects}
#         1    0.000    0.000    0.000    0.000 {method 'read' of '_io.FileIO' objects}
#         7    0.000    0.000    0.000    0.000 {method 'rpartition' of 'str' objects}
#        14    0.000    0.000    0.000    0.000 {method 'rstrip' of 'str' objects}


# PyPy 3.7.1 (with skip_str function)
#
# dads-MBP:qbjson dad$ pypy3 -m cProfile perf.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 5.687342166900635 seconds
# 25.378026784277747 MB/second
#          29540733 function calls (29540732 primitive calls) in 6.307 seconds
#
#    Ordered by: standard name
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1009(_handle_fromlist)
#         ...
#         1    0.000    0.000    0.000    0.000 jnext.py:125(pos_map)
#    117594    0.047    0.000    0.050    0.000 jnext.py:148(skip_bytes)
#  10054456    3.065    0.000    3.065    0.000 jnext.py:166(skip_str)
#         1    0.000    0.000    0.000    0.000 jnext.py:19(<module>)
#         3    0.000    0.000    0.000    0.000 jnext.py:198(skip_dec)
#   9330241    2.178    0.000    5.388    0.000 jnext.py:220(jnext)
#         1    0.000    0.000    0.000    0.000 jnext.py:344(end_src)
#         1    0.000    0.000    0.000    0.000 jnext.py:411(ParseState)
#         1    0.000    0.000    0.000    0.000 jnext.py:412(__init__)
#         1    0.000    0.000    0.000    0.000 jnext.py:437(new_ps)
#         1    0.000    0.000    6.307    6.307 perf.py:19(<module>)
#         1    0.299    0.299    5.687    5.687 perf.py:23(parse)
#         1    0.000    0.000    0.000    0.000 subprocess.py:1414(_internal_poll)
#         1    0.000    0.000    0.000    0.000 subprocess.py:793(__del__)
#        72    0.000    0.000    0.000    0.000 utf_8.py:19(encode)
#         1    0.000    0.000    0.000    0.000 {built-in function __build_class__}
#        72    0.000    0.000    0.000    0.000 {built-in function _codecs.utf_8_encode}
#         1    0.000    0.000    0.000    0.000 {built-in function _imp._fix_co_filename}
#       119    0.000    0.000    0.000    0.000 {built-in function _imp.acquire_lock}
#         1    0.000    0.000    0.000    0.000 {built-in function _imp.is_builtin}
#         1    0.000    0.000    0.000    0.000 {built-in function _imp.is_frozen}
#       119    0.000    0.000    0.000    0.000 {built-in function _imp.release_lock}
#         1    0.000    0.000    0.000    0.000 {built-in function _io.open}
#         4    0.000    0.000    0.000    0.000 {built-in function _thread.allocate_lock}
#        18    0.000    0.000    0.000    0.000 {built-in function _thread.get_ident}
#       2/1    0.000    0.000    6.307    6.307 {built-in function exec}
#         6    0.000    0.000    0.000    0.000 {built-in function getattr}
#         4    0.000    0.000    0.000    0.000 {built-in function hasattr}
#         7    0.000    0.000    0.000    0.000 {built-in function isinstance}
#         1    0.000    0.000    0.000    0.000 {built-in function iter}
#   5136366    0.040    0.000    0.040    0.000 {built-in function len}
#         1    0.000    0.000    0.000    0.000 {built-in function marshal.loads}
#         3    0.000    0.000    0.000    0.000 {built-in function posix.fspath}
#         1    0.000    0.000    0.000    0.000 {built-in function posix.getcwd}
#         3    0.000    0.000    0.000    0.000 {built-in function posix.stat}
#         2    0.000    0.000    0.000    0.000 {built-in function time.time}
#         3    0.000    0.000    0.000    0.000 {method '__new__' of 'structseqtype' objects}
#         3    0.000    0.000    0.000    0.000 {method '__setattr__' of 'stat_result' objects}
#   2450585    0.028    0.000    0.028    0.000 {method 'append' of 'list' objects}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
#         1    0.000    0.000    0.000    0.000 {method 'endswith' of 'str' objects}
#         2    0.000    0.000    0.000    0.000 {method 'from_bytes' of 'type' objects}
#       112    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
#         6    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
#         2    0.000    0.000    0.000    0.000 {method 'partition' of 'str' objects}
#   2450585    0.029    0.000    0.029    0.000 {method 'pop' of 'list' objects}
#         1    0.618    0.618    0.618    0.618 {method 'read' of '_io.BufferedReader' objects}
#         1    0.000    0.000    0.000    0.000 {method 'read' of '_io.FileIO' objects}
#        11    0.000    0.000    0.000    0.000 {method 'remove' of 'set' objects}
#         7    0.000    0.000    0.000    0.000 {method 'rpartition' of 'str' objects}
#        10    0.000    0.000    0.000    0.000 {method 'rstrip' of 'str' objects}

# Profile of PyPy 3.7.1 (embedded skip_str logic)
#
# dads-MBP:qbjson dad$ pypy3 -m cProfile perf.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 144.33352184295654 MB in 3.166304111480713 seconds
# 45.584225886457695 MB/second
#          19486169 function calls (19486168 primitive calls) in 3.715 seconds
#
#    Ordered by: standard name
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1006(_handle_fromlist)
#         ...
#         1    0.000    0.000    0.000    0.000 jnext.py:125(pos_map)
#    117594    0.048    0.000    0.050    0.000 jnext.py:148(skip_bytes)
#         1    0.000    0.000    0.000    0.000 jnext.py:19(<module>)
#         3    0.000    0.000    0.000    0.000 jnext.py:198(skip_dec)
#   9330241    2.766    0.000    2.899    0.000 jnext.py:220(jnext)
#         1    0.000    0.000    0.000    0.000 jnext.py:362(end_src)
#         1    0.000    0.000    0.000    0.000 jnext.py:429(ParseState)
#         1    0.000    0.000    0.000    0.000 jnext.py:430(__init__)
#         1    0.000    0.000    0.000    0.000 jnext.py:455(new_ps)
#         1    0.000    0.000    3.715    3.715 perf.py:19(<module>)
#         1    0.268    0.268    3.166    3.166 perf.py:23(parse)
#         1    0.000    0.000    0.000    0.000 subprocess.py:1414(_internal_poll)
#         1    0.000    0.000    0.000    0.000 subprocess.py:793(__del__)
#        18    0.000    0.000    0.000    0.000 utf_8.py:19(encode)
#         1    0.000    0.000    0.000    0.000 {built-in function __build_class__}
#        18    0.000    0.000    0.000    0.000 {built-in function _codecs.utf_8_encode}
#         1    0.000    0.000    0.000    0.000 {built-in function _imp._fix_co_filename}
#       119    0.000    0.000    0.000    0.000 {built-in function _imp.acquire_lock}
#         1    0.000    0.000    0.000    0.000 {built-in function _imp.is_builtin}
#         1    0.000    0.000    0.000    0.000 {built-in function _imp.is_frozen}
#       119    0.000    0.000    0.000    0.000 {built-in function _imp.release_lock}
#         1    0.000    0.000    0.000    0.000 {built-in function _io.open}
#         4    0.000    0.000    0.000    0.000 {built-in function _thread.allocate_lock}
#        18    0.000    0.000    0.000    0.000 {built-in function _thread.get_ident}
#       2/1    0.000    0.000    3.715    3.715 {built-in function exec}
#         6    0.000    0.000    0.000    0.000 {built-in function getattr}
#         4    0.000    0.000    0.000    0.000 {built-in function hasattr}
#         7    0.000    0.000    0.000    0.000 {built-in function isinstance}
#         1    0.000    0.000    0.000    0.000 {built-in function iter}
#   5136366    0.038    0.000    0.038    0.000 {built-in function len}
#         1    0.000    0.000    0.000    0.000 {built-in function marshal.loads}
#         3    0.000    0.000    0.000    0.000 {built-in function posix.fspath}
#         1    0.000    0.000    0.000    0.000 {built-in function posix.getcwd}
#         3    0.000    0.000    0.000    0.000 {built-in function posix.stat}
#         2    0.000    0.000    0.000    0.000 {built-in function time.time}
#         3    0.000    0.000    0.000    0.000 {method '__new__' of 'structseqtype' objects}
#         3    0.000    0.000    0.000    0.000 {method '__setattr__' of 'stat_result' objects}
#   2450585    0.024    0.000    0.024    0.000 {method 'append' of 'list' objects}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
#         1    0.000    0.000    0.000    0.000 {method 'endswith' of 'str' objects}
#         2    0.000    0.000    0.000    0.000 {method 'from_bytes' of 'type' objects}
#       112    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
#         6    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
#         2    0.000    0.000    0.000    0.000 {method 'partition' of 'str' objects}
#   2450585    0.022    0.000    0.022    0.000 {method 'pop' of 'list' objects}
#         1    0.547    0.547    0.547    0.547 {method 'read' of '_io.BufferedReader' objects}
#         1    0.000    0.000    0.000    0.000 {method 'read' of '_io.FileIO' objects}
#        11    0.000    0.000    0.000    0.000 {method 'remove' of 'set' objects}
#         7    0.000    0.000    0.000    0.000 {method 'rpartition' of 'str' objects}
#        10    0.000    0.000    0.000    0.000 {method 'rstrip' of 'str' objects}
