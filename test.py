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


def parse(s):
    print('started')
    ps = jnext.new_ps(s)
    i = 0
    while 1:
        i += 1
        # if i % 100000 == 0:
        #     print('iter', i, '   ', jnext.tokstr(ps))
        t = jnext.jnext(ps)
        # print('iter', i, '   ', jnext.tokstr(ps))
        # print(t)
        if t == 0:
            break

    print('done')

fname = '../../../dev/json-samples/cache_150mb.json'
# fname = '../../../dev/json-samples/batters_obj.json'
# fname = 'blockchain-unconfirmed.json'
with open(fname, mode='rb') as f:
    parse(f.read())
