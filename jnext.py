#!/usr/bin/python

# Software License Agreement (ISC License)
#
# Copyright (c) 2019, Matthew Voss
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

__all__ = ["new_ps", "jnext", "tokstr"]

# values for ps.pos(ition).  LSB (0x7F) are reserved for token ascii value.
POS_A_BF = 0x080  # in array, before first value
POS_A_BV = 0x100  # in array, before value
POS_A_AV = 0x180  # in array, after value
POS_O_BF = 0x200  # in object, before first key
POS_O_BK = 0x280  # in object, before key
POS_O_AK = 0x300  # in object, after key
POS_O_BV = 0x380  # in object, before value
POS_O_AV = 0x400  # in object, after value

POS2NAME = {
    POS_A_BF: "A_BF",
    POS_A_BV: "A_BV",
    POS_A_AV: "A_AV",
    POS_O_BF: "O_BF",
    POS_O_BK: "O_BK",
    POS_O_AK: "O_AK",
    POS_O_BV: "O_BV",
    POS_O_AV: "O_AV"
}

# values for ps.tok(en).  All but string and decimal are represented by the first ascii byte encountered
TOK_ARR = 91  # [    array start
TOK_ARR_END = 93  # ]    array end
TOK_DEC = 100  # d    a decimal value starting with = -, 0, 1, ..., 9
TOK_FAL = 102  # f    false
TOK_NUL = 110  # n    null
TOK_STR = 115  # s    a string value starting with "
TOK_TRU = 116  # t    true
TOK_OBJ = 123  # {    object start
TOK_OBJ_END = 125  # }    object end

# ASCII flags
NON_TOKEN = 1  # '\b\f\n\t\r ,:',
DELIM = 2  # '\b\f\n\t\r ,:{}[]',
DECIMAL_END = 4  # '0123456789',
DECIMAL_ASCII = 8  # '-0123456789+.eE',
NO_LEN_TOKENS = 16  # 'tfn[]{}()',

# for an unexpected or illegal value, or if src limit is reached before a value is complete, ps.tok will be zero
# and ps.ecode will be one of the following:
ECODE_BAD_VALUE = 66  # 'B'  encountered invalid byte or series of bytes
ECODE_TRUNC_DEC = 68  # 'D'  end of buffer was a decimal ending with a digit (0-9). it is *possibly* unfinished
ECODE_KEY_NO_VAL = 75  # 'K'  object key complete, but value did not start
ECODE_TRUNCATED = 84  # 'T'  key or value was unfinished at end of buffer
ECODE_UNEXPECTED = 85  # 'U'  encountered a recognized token in wrong place/context

#       0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
#    -----------------------------------------------------------------------------------
# 0  |  NUL  SOH  STX  ETX  EOT  ENQ  ACK  BEL  BS   TAB  LF   VT   FF   CR   SO   SI  |  # 0
# 1  |  DLE  DC1  DC2  DC3  DC4  NAK  SYN  ETB  CAN  EM   SUB  ESC  FS   GS   RS   US  |  # 1
# 2  |  SPC  !    "    #    $    %    &    '    (    )    *    +    ,    -    .    /   |  # 2
# 3  |  0    1    2    3    4    5    6    7    8    9    :    ;    <    =    >    ?   |  # 3
# 4  |  @    A    B    C    D    E    F    G    H    I    J    K    L    M    N    O   |  # 4
# 5  |  P    Q    R    S    T    U    V    W    X    Y    Z    [    \    ]    ^    _   |  # 5
# 6  |  `    a    b    c    d    e    f    g    h    i    j    k    l    m    n    o   |  # 6
# 7  |  p    q    r    s    t    u    v    w    x    y    z    {    |    }    ~        |  # 7
#    -----------------------------------------------------------------------------------

# CMAP was lovingly crafted by util.js
#   0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F
CMAP = [
    0, 0, 0, 0, 0, 0, 0, 0, 0x03, 0x03, 0x03, 0, 0x03, 0x03, 0, 0,  # 0
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 1
    0x03, 0, 0, 0, 0, 0, 0, 0, 0x10, 0x10, 0, 0x08, 0x03, 0x08, 0x08, 0,  # 2
    0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x03, 0, 0, 0, 0, 0,  # 3
    0, 0, 0, 0, 0, 0x08, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 4
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x12, 0, 0x12, 0, 0,  # 5
    0, 0, 0, 0, 0, 0x08, 0x10, 0, 0, 0, 0, 0, 0, 0, 0x10, 0,  # 6
    0, 0, 0, 0, 0x10, 0, 0, 0, 0, 0, 0, 0x12, 0, 0x12, 0, 0,  # 7
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 8
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 9
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # A
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # B
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # C
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # D
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # E
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # F
]

# for an unexpected or illegal value, or if src limit is reached before a value is complete, ps.tok will be zero
# and ps.ecode will be one of the following:
ECODE = {
    'BAD_VALUE': 66,  # 'B'  encountered invalid byte or series of bytes
    'TRUNC_DEC': 68,  # 'D'  end of buffer was a decimal ending with a digit (0-9). it is *possibly* unfinished
    'KEY_NO_VAL': 75,  # 'K'  object key complete, but value did not start
    'TRUNCATED': 84,  # 'T'  key or value was unfinished at end of buffer
    'UNEXPECTED': 85,  # 'U'  encountered a recognized token in wrong place/context
}


def as_buffer(s):
    return s


#    return Uint8Array.from(s.split('').map(function (c) { return c.charCodeAt(0) }))


TOK_BYTES = {102: b'alse', 110: b'ull', 116: b'rue'}


def posname(pos): return POS2NAME[pos] or '???'


def pos_map():
    ret = [0] * (0x400 + 0xFF)
    # pos_pairs is generated by utils.js. map first to second as in 219 -> 128, 221 -> 384, etc...
    pos_pairs = [
        219, 128, 221, 384, 228, 384, 230, 384, 238, 384, 243, 384, 244, 384, 251, 512,
        347, 128, 356, 384, 358, 384, 366, 384, 371, 384, 372, 384, 379, 512, 428, 256,
        477, 384, 627, 768, 637, 384, 755, 768, 826, 896, 987, 128, 996, 1024, 998, 1024,
        1006, 1024, 1011, 1024, 1012, 1024, 1019, 512, 1068, 640, 1149, 384,
    ]
    it = iter(pos_pairs)
    for k, v in zip(it, it):
        ret[k] = v

    return ret


POS_MAP = pos_map()


# skip as many bytes of src that match bsrc, up to lim.
# return
#     i    the new index after all bytes are matched (past matched bytes)
#    -i    (negative) the index of the first unmatched byte (past matched bytes)
def skip_bytes(src, off, lim, bsrc):
    """
    >>> skip_bytes(b' true, ', 2, 9, b'rue')
    5
    """
    blen = len(bsrc)
    if blen > lim - off:
        blen = lim - off
    i = 0
    while i < blen and bsrc[i] == src[i + off]:
        i += 1
    return i + off if i == len(bsrc) else -(i + off)

MASK = bytearray(256)
MASK[34] = 1
MASK[92] = 1
# noinspection PyShadowingNames
# Return the index of the next unescaped double-quote.
def skip_str(src, off, lim):
    """
    use unicode 5C for backslash because backslash-escapes within quoted tests is buggy.
    >>> skip_str(u'""', 1, 99)
    2
    >>> skip_str('"a"', 1, 99)
    3
    # >>> skip_str(u'"\u005C', 1, 2)
    # -2
    >>> skip_str(u'"\u005C\u005C', 1, 3)
    -3
    >>> skip_str(u'"\u005C\u005C"', 1, 99)
    4
    >>> skip_str(u'"\u005C\u005C\u005C"', 1, 5)
    -5
    >>> skip_str(u'"\u005C\u005C\u005C""', 1, 99)
    6
    """
    i = off
    mask = MASK
    while i < lim:
        if mask[src[i]] == 0:
            i += 1
        elif src[i] == 34:
            return i + 1
        elif src[i] == 92:
            if i == lim - 1:
                return -lim
            i += 2
    return -lim


def skip_dec(src, off, lim):
    while off < lim and (CMAP[src[off]] & DECIMAL_ASCII):
        off += 1
    return off if off < lim and (CMAP[src[off]] & DELIM) else -off


# switch ps.src to ps.next_src if conditions are right (ps.src is None or is complete without errors)
def next_src(ps):
    if ps.ecode or (ps.src and ps.vlim < ps.lim):
        return False
    if len(ps.next_src) == 0:
        ps.next_src = None
        return False

    ps.soff += ps.src and len(ps.src) or 0
    ps.src = ps.next_src
    ps.next_src = None
    ps.koff = ps.klim = ps.voff = ps.vlim = ps.tok = ps.ecode = 0
    ps.lim = len(ps.src)
    return True


def jnext(ps, opt=None):
    if ps.ecode != 0:  # ecode is sticky (requires intentional fix)
        ps.tok = 0
        return 0

    ps.koff = ps.klim = ps.voff = ps.vlim
    src = ps.src
    while ps.vlim < ps.lim:
        ps.voff = ps.vlim
        ps.tok = src[ps.vlim]
        ps.vlim += 1

        # "    QUOTE
        if ps.tok == 34:
            ps.tok = 115  # s for string

            mask = MASK
            i = ps.vlim
            lim = ps.lim
            while i < lim:
                if mask[src[i]] == 0:
                    i += 1
                elif src[i] == 34:
                    ps.vlim = i + 1
                    break
                elif src[i] == 92:
                    if i == lim - 1:
                        ps.vlim = -i
                        break
                    i += 2
            if i == lim:
                ps.lim = -i

            pos1 = POS_MAP[ps.pos | ps.tok]
            if pos1 == 0:
                return handle_unexp(ps, opt)
            if pos1 == POS_O_AK:
                # key
                ps.koff = ps.voff
                if ps.vlim > 0:
                    ps.pos = pos1
                    ps.klim = ps.voff = ps.vlim
                    continue
                else:
                    ps.klim = ps.voff = -ps.vlim
                    return handle_neg(ps, opt)
            else:
                # value
                if ps.vlim > 0:
                    ps.pos = pos1
                    ps.vcount += 1
                    return ps.tok
                else:
                    return handle_neg(ps, opt)

        # ,    COMMA
        # :    COLON
        if ps.tok == 44 or ps.tok == 58:
            pos1 = POS_MAP[ps.pos | ps.tok]
            if pos1 == 0:
                ps.voff = ps.vlim - 1
                return handle_unexp(ps, opt)
            ps.pos = pos1
            continue

        # [    ARRAY START  { OBJECT START
        if ps.tok == 91 or ps.tok == 123:
            pos1 = POS_MAP[ps.pos | ps.tok]
            if pos1 == 0:
                return handle_unexp(ps, opt)
            ps.pos = pos1
            ps.stack.append(ps.tok)
            return ps.tok

        # ]   ARRAY END
        if ps.tok == 93:
            if POS_MAP[ps.pos | ps.tok] == 0:
                return handle_unexp(ps, opt)
            ps.stack.pop()
            ps.pos = POS_O_AV if len(ps.stack) and ps.stack[len(ps.stack) - 1] == 123 else POS_A_AV
            ps.vcount += 1
            return ps.tok

        # }    OBJECT END
        if ps.tok == 125:
            if POS_MAP[ps.pos | ps.tok] == 0:
                return handle_unexp(ps, opt)
            ps.stack.pop()
            ps.pos = POS_O_AV if len(ps.stack) and ps.stack[len(ps.stack) - 1] == 123 else POS_A_AV
            ps.vcount += 1
            return ps.tok

        if ps.tok == 10:
            ps.lineoff = ps.soff + ps.vlim
            ps.line += 1
            continue

        if ps.tok == 13:
            ps.lineoff = ps.soff + ps.vlim
            continue

        if ps.tok == 8 or ps.tok == 9 or ps.tok == 12 or ps.tok == 32:  # other white-space
            continue

        # f and t   false
        if ps.tok == 102 or ps.tok == 110 or ps.tok == 116:
            ps.vlim = skip_bytes(src, ps.vlim, ps.lim, TOK_BYTES[ps.tok])
            pos1 = POS_MAP[ps.pos | ps.tok]
            if pos1 == 0:
                return handle_unexp(ps, opt)
            if ps.vlim > 0:
                ps.pos = pos1
                ps.vcount += 1
                return ps.tok
            else:
                return handle_neg(ps, opt)

        # digits 0-9 and '-'
        if (48 <= ps.tok <= 57) or ps.tok == 45:
            ps.tok = 100  # d for decimal
            ps.vlim = skip_dec(src, ps.vlim, ps.lim)
            pos1 = POS_MAP[ps.pos | ps.tok]
            if pos1 == 0:
                return handle_unexp(ps, opt)
            if ps.vlim > 0:
                ps.pos = pos1
                ps.vcount += 1
                return ps.tok
            else:
                return handle_neg(ps, opt)

        ps.vlim -= 1
        ps.ecode = ECODE_BAD_VALUE
        return end_src(ps, opt)

    # reached src limit without error or truncation
    if CMAP[ps.tok] & NON_TOKEN:
        ps.voff = ps.vlim

    return end_src(ps, opt)


def end_src(ps, opt):
    if ps.ecode == 0:
        if ps.pos == POS_O_AK or ps.pos == POS_O_BV:
            ps.ecode = ECODE_KEY_NO_VAL
        elif ps.next_src and next_src(ps):
            return next(ps)

    elif ps.ecode == ECODE_BAD_VALUE or ps.ecode == ECODE_UNEXPECTED:
        ps.tok = 0
        checke(ps)
        # any other ecode is just sticky (prevents progress)

    ps.tok = 0
    return ps.tok


def handle_neg(ps, opt):
    ps.vlim = -ps.vlim
    if ps.vlim >= ps.lim:
        ps.ecode = ECODE_TRUNC_DEC \
            if ps.tok == TOK_DEC and (CMAP[ps.src[ps.vlim - 1]] & DECIMAL_END) \
            else ECODE_TRUNCATED
    else:
        ps.ecode = ECODE_BAD_VALUE
    ps.vlim += 1
    return end_src(ps, opt)


def handle_unexp(ps, opt):
    if ps.vlim < 0:
        ps.vlim = -ps.vlim
    ps.ecode = ECODE_UNEXPECTED
    return end_src(ps, opt)


def err(msg, ps):
    ctx = 'line ' + str(ps.line) + ', col ' + str(ps.soff + ps.voff - ps.lineoff + 1) + ', tokstr ' + tokstr(ps, True)
    e = Exception(msg + ': ' + ctx)
    e.parse_state = ps
    raise e


def checke(ps):
    ps.ecode != ECODE_UNEXPECTED or err('unexpected token at ' + str(ps.voff) + '..' + str(ps.vlim), ps)
    ps.ecode != ECODE_BAD_VALUE or err('bad value "' + bytes2str(ps.src, ps.voff, ps.vlim) + '" at ' + str(ps.voff) + '..' + str(ps.vlim), ps)

def bytes2str(src, off, lim):
    slice = src[off:lim]
    return ''.join(map(chr, slice))

def tokstr(ps, detail=False):
    keystr = '' if ps.koff == ps.klim else 'k' + str(ps.klim - ps.koff) + '@' + str(ps.koff) + ':'
    vlen = '' if (ps.vlim == ps.voff or (CMAP[ps.tok] & NO_LEN_TOKENS)) else ps.vlim - ps.voff

    tchar = ps.tok and chr(ps.tok) or '!'
    ret = keystr + tchar + str(vlen) + '@' + str(ps.voff)
    if ps.ecode:
        ret += ':' + chr(ps.ecode)

    if detail:
        ret += ':' + posname(ps.pos)
        if len(ps.stack):
            ret += ':' + ''.join(map(chr, ps.stack))

    return ret


class ParseState(object):
    def __init__(self, src, off=0, lim=-1):
        self.src = src
        self.soff = off
        self.lim = lim if lim > -1 else len(src)
        self.koff = 0
        self.klim = 0
        self.voff = 0
        self.vlim = 0
        self.tok = 0
        self.stack = []
        self.pos = POS_A_BF
        self.ecode = 0
        self.vcount = 0
        self.line = 1
        self.lineoff = 0
        self.next_src = None

    def setsrc(self, v):
        self.src = v
        self.soff = 0
        self.lim = len(v)

    def __str__(self):
        return str(self.__dict__)

def new_ps(src, off=0, lim=-1):
    return ParseState(src, off, lim)


if __name__ == "__main__":
    import doctest
    doctest.testmod()