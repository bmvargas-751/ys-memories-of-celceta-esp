"""Compresión de Falcom (FALCOM2 / FALCOM3, «BZ mode 2») usada en Celceta.

Formato deducido del compresor de flame (heroesoflegend.org), portado por
uyjulian: https://gist.github.com/uyjulian/ba631cbba7025806c5e356daeb3c9507

FALCOM3: u32 tamaño-4, u32 tamaño descomprimido, u32 bloques (+1),
y por cada bloque u16 (largo+2) y sus datos FALCOM2; entre bloques un byte
0x01 y al final un 0x00.

FALCOM2: banderas en palabras u16 (la primera solo usa 8 bits, del bit 8 al 15;
las demás, los 16 desde el bit 0). Cada byte del flujo se lee después del bit
que le sigue en el compresor, y la palabra siguiente se carga cuando hace falta.
"""
import struct


class _Reader:
    def __init__(self, data):
        self.d = data
        self.p = 0
        self.flags = 0
        self.left = 0
        self.first = True

    def byte(self):
        b = self.d[self.p]
        self.p += 1
        return b

    def bit(self):
        if self.left == 0:
            w = struct.unpack_from("<H", self.d, self.p)[0]
            self.p += 2
            if self.first:
                self.flags, self.left, self.first = w >> 8, 8, False
            else:
                self.flags, self.left = w, 16
        b = self.flags & 1
        self.flags >>= 1
        self.left -= 1
        return b

    def bits(self, n):
        v = 0
        for _ in range(n):
            v = (v << 1) | self.bit()
        return v


def decompress_falcom2(data):
    r = _Reader(data)
    out = bytearray()
    while True:
        if r.bit() == 0:
            out.append(r.byte())
            continue
        if r.bit() == 0:
            off = r.byte()
        else:
            hi = r.bits(5)
            lo = r.byte()
            off = (hi << 8) | lo
            if off == 0:
                break
            if off == 1:  # repetición de un byte
                if r.bit() == 0:
                    n = r.bits(4)
                    val = r.byte()
                else:
                    hi = r.bits(4)
                    lo = r.byte()
                    val = r.byte()
                    n = (hi << 8) | lo
                out += bytes([val]) * (n + 0xE)
                continue
        # largo de la copia
        zeros = 0
        while zeros < 4 and r.bit() == 0:
            zeros += 1
        if zeros < 4:
            size = 2 + zeros
        elif r.bit() == 0:
            size = r.byte() + 0xE
        else:
            size = r.bits(3) + 6
        for _ in range(size):
            out.append(out[-off])
    return bytes(out), r.p


def decompress_falcom3(data):
    """data empieza en el campo «tamaño-4». Devuelve (datos, bytes consumidos)."""
    csize, usize, nchunks = struct.unpack_from("<III", data, 0)
    p = 12
    out = bytearray()
    while True:
        clen = struct.unpack_from("<H", data, p)[0]
        chunk = data[p + 2:p + clen]
        dec, _ = decompress_falcom2(chunk)
        out += dec
        p += clen
        cont = data[p]
        p += 1
        if cont == 0:
            break
    # El compresor de Falcom deja un bloque final de 1 byte que el juego
    # descarta: manda el tamaño de la cabecera.
    if len(out) < usize:
        raise ValueError(f"FALCOM3: salen {len(out)} bytes, la cabecera dice {usize}")
    out = out[:usize]
    if p != csize + 4:
        raise ValueError(f"FALCOM3: se leyeron {p} bytes, la cabecera dice {csize + 4}")
    return bytes(out), p


# ---------------------------------------------------------------- compresión

class _Writer:
    """Escribe el flujo en el mismo orden en que lo lee _Reader."""

    def __init__(self):
        self.out = bytearray()
        self.fpos = None
        self.left = 0
        self.shift = 0
        self.first = True

    def bit(self, b):
        if self.left == 0:
            self.fpos = len(self.out)
            self.out += b"\0\0"
            if self.first:
                self.left, self.shift, self.first = 8, 8, False
            else:
                self.left, self.shift = 16, 0
        if b:
            w = struct.unpack_from("<H", self.out, self.fpos)[0] | (1 << self.shift)
            struct.pack_into("<H", self.out, self.fpos, w)
        self.shift += 1
        self.left -= 1

    def byte(self, x):
        self.out.append(x)


def compress_falcom2_literal(data):
    """FALCOM2 sin buscar repeticiones: cada byte va como literal (válido y simple)."""
    w = _Writer()
    for x in data:
        w.bit(0)
        w.byte(x)
    # fin: copia larga con desplazamiento 0
    w.bit(1)
    w.bit(1)
    for _ in range(5):
        w.bit(0)
    w.byte(0)
    return bytes(w.out)


CHUNK = 0x7000   # sin comprimir por bloque: comprimido queda por debajo de 0x7FF0


def compress_falcom3(data):
    chunks = [compress_falcom2_literal(data[i:i + CHUNK]) for i in range(0, len(data), CHUNK)] or \
        [compress_falcom2_literal(b"")]
    body = bytearray()
    for k, c in enumerate(chunks):
        if k:
            body.append(1)
        body += struct.pack("<H", len(c) + 2) + c
    body.append(0)
    total = 12 + len(body)
    return struct.pack("<III", total - 4, len(data), len(chunks)) + bytes(body)
