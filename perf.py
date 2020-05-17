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
      print('parsed', count, 'tokens')
    if not jnext.jnext(ps):
      break

  return (time.time() - t0) * 1000

fname = '../../../dev/json-samples/cache_150mb.json'
# fname = '../../../dev/json-samples/batters_obj.json'
with open(fname, mode='rb') as f:
  buf = f.read()
  print('read', f.name)
  ps = jnext.new_ps(buf)
  total_ms = parse(ps)
  print('parsed', len(buf)/(1024*1024), 'MB in', total_ms/1000, 'seconds')

print(len(buf) / ((total_ms/1000) * 1024 * 1024), 'MB/second')

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

# dads-MBP:qbjson dad$ python3 -m cProfile perf.py
# read ../../../dev/json-samples/cache_150mb.json
# parsed 1000000 tokens
# parsed 2000000 tokens
# parsed 3000000 tokens
# parsed 4000000 tokens
# parsed 5000000 tokens
# parsed 6000000 tokens
# parsed 7000000 tokens
# parsed 8000000 tokens
# parsed 9000000 tokens
# parsed 144.33352184295654 MB in 86.63806891441345 seconds
# 1.6659365063357805 MB/second
#          64967827 function calls (64967826 primitive calls) in 86.718 seconds
#
#    Ordered by: standard name
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:103(release)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:143(__init__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:147(__enter__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:151(__exit__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:157(_get_module_lock)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:176(cb)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:211(_call_with_frames_removed)
#         7    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:222(_verbose_message)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:307(__init__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:311(__enter__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:318(__exit__)
#         4    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:321(<genexpr>)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:35(_new_module)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:369(__init__)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:403(cached)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:416(parent)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:424(has_location)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:504(_init_module_attrs)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:576(module_from_spec)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:58(__init__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:663(_load_unlocked)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:719(find_spec)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:78(acquire)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:792(find_spec)
#         3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:855(__enter__)
#         3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:859(__exit__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:882(_find_spec)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:978(_find_and_load)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1203(_path_importer_cache)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1272(find_spec)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1351(_get_spec)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:271(cache_from_source)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:36(_relax_case)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:369(_get_cached)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:401(_check_name_wrapper)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:438(_classify_pyc)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:471(_validate_timestamp_pyc)
#         3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:51(_r_long)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:523(_compile_bytecode)
#         6    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:56(_path_join)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:574(spec_from_file_location)
#         6    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:58(<listcomp>)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:62(_path_split)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:719(create_module)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:722(exec_module)
#         3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:74(_path_stat)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:793(get_code)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:84(_path_is_mode_type)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:884(__init__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:909(get_filename)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:914(get_data)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:93(_path_isfile)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:951(path_stats)
#         1    0.000    0.000    0.000    0.000 jnext.py:125(pos_map)
#    117594    0.129    0.000    0.148    0.000 jnext.py:148(skip_bytes)
#  10054456   23.298    0.000   23.298    0.000 jnext.py:164(skip_str)
#         1    0.000    0.000    0.000    0.000 jnext.py:19(<module>)
#         3    0.000    0.000    0.000    0.000 jnext.py:195(skip_dec)
#   9330241   55.145    0.000   83.242    0.000 jnext.py:217(jnext)
#         1    0.000    0.000    0.000    0.000 jnext.py:341(end_src)
#         1    0.000    0.000    0.000    0.000 jnext.py:408(ParseState)
#         1    0.000    0.000    0.000    0.000 jnext.py:409(__init__)
#  35427812    3.798    0.000    3.798    0.000 jnext.py:431(getsrc)
#         1    0.000    0.000    0.000    0.000 jnext.py:441(new_ps)
#         1    0.000    0.000   86.718   86.718 perf.py:19(<module>)
#         1    3.396    3.396   86.638   86.638 perf.py:23(parse)
#         1    0.000    0.000    0.000    0.000 {built-in method _imp._fix_co_filename}
#         5    0.000    0.000    0.000    0.000 {built-in method _imp.acquire_lock}
#         1    0.000    0.000    0.000    0.000 {built-in method _imp.is_builtin}
#         1    0.000    0.000    0.000    0.000 {built-in method _imp.is_frozen}
#         5    0.000    0.000    0.000    0.000 {built-in method _imp.release_lock}
#         2    0.000    0.000    0.000    0.000 {built-in method _thread.allocate_lock}
#         2    0.000    0.000    0.000    0.000 {built-in method _thread.get_ident}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.any}
#       2/1    0.000    0.000   86.718   86.718 {built-in method builtins.exec}
#         6    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
#         3    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
#         2    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.iter}
#   5136363    0.391    0.000    0.391    0.000 {built-in method builtins.len}
#        12    0.000    0.000    0.000    0.000 {built-in method builtins.print}
#         3    0.000    0.000    0.000    0.000 {built-in method from_bytes}
#         1    0.000    0.000    0.000    0.000 {built-in method io.open}
#         1    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
#         3    0.000    0.000    0.000    0.000 {built-in method posix.fspath}
#         1    0.000    0.000    0.000    0.000 {built-in method posix.getcwd}
#         3    0.000    0.000    0.000    0.000 {built-in method posix.stat}
#         2    0.000    0.000    0.000    0.000 {built-in method time.time}
#   2450585    0.219    0.000    0.219    0.000 {method 'append' of 'list' objects}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
#         1    0.000    0.000    0.000    0.000 {method 'endswith' of 'str' objects}
#         2    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
#         8    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
#   2450585    0.263    0.000    0.263    0.000 {method 'pop' of 'list' objects}
#         1    0.079    0.079    0.079    0.079 {method 'read' of '_io.BufferedReader' objects}
#         1    0.000    0.000    0.000    0.000 {method 'read' of '_io.FileIO' objects}
#         7    0.000    0.000    0.000    0.000 {method 'rpartition' of 'str' objects}
#        14    0.000    0.000    0.000    0.000 {method 'rstrip' of 'str' objects}