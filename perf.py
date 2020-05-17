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

  return time.time() - t0

from array import array
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

# SLOW CPython Test Result on 2014 Macbook Pro: 2020-05-16 (CPython 3.7.7)
#
# dads-MBP:qbjson dad$ python3 perf.py
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
# parsed 144.33352184295654 MB in 57.78302001953125 seconds
# 2.4978535527248376 MB/second
# dads-MBP:qbjson dad$

# OK PyPy Test result on 2014 Macbook Pro: 2020-05-16 (PyPy 3.7.1)
#
# dads-MBP:qbjson dad$ pypy3 perf.py
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
# parsed 144.33352184295654 MB in 1.4544610977172852 seconds
# 99.23505143553298 MB/second

# EVEN FASTER NODE JS test result (see qb-json-next)
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

# PROFILE of CPython
# dads-MBP:qbjson dad$ python3 -m cProfile perf.py
#
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
# parsed 144.33352184295654 MB in 62.46955704689026 seconds
# 2.310461745944803 MB/second
#          29540265 function calls (29540259 primitive calls) in 62.557 seconds
#
#    Ordered by: standard name
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1009(_handle_fromlist)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:103(release)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:143(__init__)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:147(__enter__)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:151(__exit__)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:157(_get_module_lock)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:176(cb)
#       4/2    0.000    0.000    0.004    0.002 <frozen importlib._bootstrap>:211(_call_with_frames_removed)
#        28    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:222(_verbose_message)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:307(__init__)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:311(__enter__)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:318(__exit__)
#         8    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:321(<genexpr>)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:35(_new_module)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:369(__init__)
#         3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:403(cached)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:416(parent)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:424(has_location)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:504(_init_module_attrs)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:576(module_from_spec)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:58(__init__)
#       2/1    0.000    0.000    0.004    0.004 <frozen importlib._bootstrap>:663(_load_unlocked)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:719(find_spec)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:78(acquire)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:792(find_spec)
#         6    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:855(__enter__)
#         6    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:859(__exit__)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:882(_find_spec)
#       2/1    0.000    0.000    0.004    0.004 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
#       2/1    0.000    0.000    0.004    0.004 <frozen importlib._bootstrap>:978(_find_and_load)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1029(__init__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1040(create_module)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1048(exec_module)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:105(_write_atomic)
#         6    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1203(_path_importer_cache)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1272(find_spec)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1351(_get_spec)
#         5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:271(cache_from_source)
#         5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:36(_relax_case)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:369(_get_cached)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:381(_calc_mode)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:401(_check_name_wrapper)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:438(_classify_pyc)
#         3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:46(_w_long)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:471(_validate_timestamp_pyc)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:51(_r_long)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:536(_code_to_timestamp_pyc)
#        22    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:56(_path_join)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:574(spec_from_file_location)
#        22    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:58(<listcomp>)
#         3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:62(_path_split)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:719(create_module)
#         1    0.000    0.000    0.004    0.004 <frozen importlib._bootstrap_external>:722(exec_module)
#        10    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:74(_path_stat)
#         1    0.000    0.000    0.003    0.003 <frozen importlib._bootstrap_external>:785(source_to_code)
#         1    0.000    0.000    0.004    0.004 <frozen importlib._bootstrap_external>:793(get_code)
#         3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:84(_path_is_mode_type)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:884(__init__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:909(get_filename)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:914(get_data)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:93(_path_isfile)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:951(path_stats)
#         1    0.000    0.000    0.001    0.001 <frozen importlib._bootstrap_external>:956(_cache_bytecode)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:961(set_data)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:98(_path_isdir)
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

# Profile of PyPy
# dads-MBP:qbjson dad$ pypy3 -m cProfile perf.py
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
# parsed 144.33352184295654 MB in 5.687342166900635 seconds
# 25.378026784277747 MB/second
#          29540733 function calls (29540732 primitive calls) in 6.307 seconds
#
#    Ordered by: standard name
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1006(_handle_fromlist)
#         3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap>:1071(__import__)
#         9    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:112(release)
#         5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:152(__init__)
#         5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:156(__enter__)
#         5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:160(__exit__)
#         9    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:166(_get_module_lock)
#       107    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:185(cb)
#         4    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:203(_lock_unlock_module)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:220(_call_with_frames_removed)
#         5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:231(_verbose_message)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:316(__init__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:320(__enter__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:327(__exit__)
#         4    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:330(<genexpr>)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:35(_new_module)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:378(__init__)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:412(cached)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:425(parent)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:433(has_location)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:513(_init_module_attrs)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:573(module_from_spec)
#         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:58(__init__)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:660(_load_unlocked)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:716(find_spec)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:789(find_spec)
#         3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:852(__enter__)
#         3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:856(__exit__)
#         9    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:87(acquire)
#         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:879(_find_spec)
#         5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:926(_sanity_check)
#         1    0.000    0.000    0.001    0.001 <frozen importlib._bootstrap>:945(_find_and_load_unlocked)
#         5    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap>:975(_find_and_load)
#         5    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap>:991(_gcd_import)
#        11    0.000    0.000    0.000    0.000 _weakrefset.py:26(__exit__)
#         6    0.000    0.000    0.000    0.000 _weakrefset.py:52(_commit_removals)
#        11    0.000    0.000    0.000    0.000 _weakrefset.py:58(__iter__)
#        20    0.000    0.000    0.000    0.000 frozen _structseq:22(__get__)
#         3    0.000    0.000    0.000    0.000 frozen _structseq:77(structseq_new)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:1093(_path_importer_cache)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:1130(_get_spec)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:1162(find_spec)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:1241(_get_spec)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:1246(find_spec)
#         2    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:276(cache_from_source)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:37(_relax_case)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:374(_get_cached)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:406(_check_name_wrapper)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:443(_validate_bytecode_header)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:498(_compile_bytecode)
#         2    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:52(_r_long)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:537(spec_from_file_location)
#         4    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:57(_path_join)
#         4    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:59(<listcomp>)
#         2    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:63(_path_split)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:682(create_module)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:685(exec_module)
#         3    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:75(_path_stat)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:756(get_code)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:813(__init__)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:838(get_filename)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:843(get_data)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:85(_path_is_mode_type)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:853(path_stats)
#         1    0.000    0.000    0.000    0.000 frozen importlib._bootstrap_external:94(_path_isfile)
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