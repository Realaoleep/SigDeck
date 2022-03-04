"""Pure-Python Ed25519 (RFC 8032) - readable, stdlib-only."""

import hashlib

P = 2 ** 255 - 19
L = 2 ** 252 + 27742317777372353535851937790883648493
D = -121665 * pow(121666, P - 2, P) % P


def _inv(a):
    return pow(a, P - 2, P)


def _xrecover(y):
    xx = (y * y - 1) * _inv(D * y * y + 1) % P
    x = pow(xx, (P + 3) // 8, P)
    if x % 2:
        x = P - x
    return x


_BY = 4 * _inv(5) % P
B = (_xrecover(_BY), _BY)


def _encodepoint(point):
    x, y = point
    bits = [(y >> i) & 1 for i in range(255)] + [x & 1]
    return bytes(sum(bits[i * 8 + j] << j for j in range(8)) for i in range(32))


def _point_add(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x3 = (x1 * y2 + y1 * x2) * _inv(1 + D * x1 * x2 * y1 * y2) % P
    y3 = (y1 * y2 + x1 * x2) * _inv(1 - D * x1 * x2 * y1 * y2) % P
    return (x3, y3)


def _scalarmult(point, e):
    if e == 0:
        return (0, 1)
    q = _scalarmult(point, e >> 1)
    q = _point_add(q, q)
    if e & 1:
        q = _point_add(q, point)
    return q


def sign(message, seed):
    h = hashlib.sha512(seed).digest()
    a = int.from_bytes(h[:32], "little") & ((1 << 254) - 8) | (1 << 254)
    prefix = h[32:]
    a_point = _encodepoint(_scalarmult(B, a))
    r = int.from_bytes(hashlib.sha512(prefix + message).digest(), "little") % L
    r_point = _encodepoint(_scalarmult(B, r))
    h2 = int.from_bytes(hashlib.sha512(r_point + a_point + message).digest(), "little") % L
    s = (r + h2 * a) % L
    return r_point + s.to_bytes(32, "little")


def verify(signature, message, public):
    if len(signature) != 64:
        return False
    r_point = _decodepoint(signature[:32])
    a_point = _decodepoint(public)
    h = int.from_bytes(hashlib.sha512(signature[:32] + public + message).digest(), "little") % L
    s = int.from_bytes(signature[32:], "little")
    return _encodepoint(_scalarmult(B, s)) == _encodepoint(
        _point_add(r_point, _scalarmult(a_point, h)))


def _decodepoint(s):
    y = int.from_bytes(s, "little") & ((1 << 255) - 1)
    x = _xrecover(y)
    if x & 1 != (s[31] >> 7):
        x = P - x
    return (x, y)
