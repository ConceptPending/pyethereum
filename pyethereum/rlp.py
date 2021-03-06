def to_binary_array(n):
    if n == 0:
        return []
    else:
        x = to_binary_array(n / 256)
        x.append(n % 256)
        return x


def to_binary(n):
    return ''.join([chr(x) for x in to_binary_array(n)])


def from_binary(b):
    if len(b) == 0:
        return 0
    else:
        return from_binary(b[:-1]) * 256 + ord(b[-1])


def __decode(s, pos=0):
    assert pos < len(s), "read beyond end of string in __decode"

    fchar = ord(s[pos])
    if fchar < 128:
        return (s[pos], pos + 1)
    elif fchar < 184:
        b = fchar - 128
        return (s[pos + 1:pos + 1 + b], pos + 1 + b)
    elif fchar < 192:
        b = fchar - 183
        b2 = from_binary(s[pos + 1:pos + 1 + b])
        return (s[pos + 1 + b:pos + 1 + b + b2], pos + 1 + b + b2)
    elif fchar < 248:
        o = []
        pos += 1
        pos_end = pos + fchar - 192

        while pos < pos_end:
            obj, pos = __decode(s, pos)
            o.append(obj)
        assert pos == pos_end, "read beyond list boundary in __decode"
        return (o, pos)
    else:
        b = fchar - 247
        b2 = from_binary(s[pos + 1:pos + 1 + b])
        o = []
        pos += 1 + b
        pos_end = pos + b2
        while pos < pos_end:
            obj, pos = __decode(s, pos)
            o.append(obj)
        assert pos == pos_end, "read beyond list boundary in __decode"
        return (o, pos)


def decode(s):
    if s:
        return __decode(s)[0]


def encode_length(L, offset):
    if L < 56:
        return chr(L + offset)
    elif L < 256 ** 8:
        BL = to_binary(L)
        return chr(len(BL) + offset + 55) + BL
    else:
        raise Exception("input too long")


def encode(s):
    if isinstance(s, (str, unicode)):
        s = str(s)
        if len(s) == 1 and ord(s) < 128:
            return s
        else:
            return encode_length(len(s), 128) + s
    elif isinstance(s, list):
        output = ''
        for item in s:
            output += encode(item)
        return encode_length(len(output), 192) + output
    raise TypeError("Encoding of %s not supported" % type(s))
