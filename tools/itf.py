"""Fuente .itf de Celceta (lang/en/system/font.itf): leer y escribir glifos.

Formato:
- u16 tamaño (64), u16 número de glifos (8808), 12 bytes en cero.
- u32 offset de cada glifo desde el inicio del archivo. Un glifo vacío tiene
  el mismo offset que el siguiente.
- Glifo: u8 ancho, u8 alto, u8 desplazamiento vertical (desde arriba de la
  línea), u8 desplazamiento horizontal, u8 avance; y los píxeles a 4 bits,
  seguidos sin relleno por fila (nibble bajo primero).

Índice del glifo: ASCII 0x20-0x7E → 0-94; katakana de medio ancho 0xA1-0xDF →
95-157; dos bytes Shift-JIS → 158 + (fila JIS - 1) * 94 + (columna - 1).
"""
import struct


class Glyph:
    __slots__ = ("w", "h", "yoff", "xoff", "adv", "px")

    def __init__(self, w, h, yoff, xoff, adv, px):
        self.w, self.h, self.yoff, self.xoff, self.adv = w, h, yoff, xoff, adv
        self.px = px  # lista de filas, cada una lista de valores 0-15

    @classmethod
    def parse(cls, data):
        w, h, yoff, xoff, adv = data[:5]
        raw = data[5:]
        px = []
        for y in range(h):
            row = []
            for x in range(w):
                n = y * w + x
                row.append((raw[n // 2] >> (4 * (n % 2))) & 15)
            px.append(row)
        return cls(w, h, yoff, xoff, adv, px)

    def to_bytes(self):
        flat = [v for row in self.px for v in row]
        if len(flat) % 2:
            flat.append(0)
        raw = bytes(flat[i] | (flat[i + 1] << 4) for i in range(0, len(flat), 2))
        return bytes([self.w, self.h, self.yoff, self.xoff, self.adv]) + raw


class ITF:
    def __init__(self, data):
        self.size, n = struct.unpack_from("<HH", data, 0)
        self.head = data[:16]
        offs = list(struct.unpack_from(f"<{n}I", data, 16)) + [len(data)]
        self.raw = [data[offs[i]:offs[i + 1]] for i in range(n)]

    def __len__(self):
        return len(self.raw)

    def glyph(self, i):
        return Glyph.parse(self.raw[i]) if self.raw[i] else None

    def set_glyph(self, i, g):
        self.raw[i] = g.to_bytes()

    def build(self):
        n = len(self.raw)
        out = bytearray(self.head)
        p = 16 + 4 * n
        offs = []
        for r in self.raw:
            offs.append(p)
            p += len(r)
        out += struct.pack(f"<{n}I", *offs)
        for r in self.raw:
            out += r
        return bytes(out)


def index(b):
    if len(b) == 1:
        return b[0] - 0x20 if b[0] < 0x80 else 95 + b[0] - 0xA1
    s1, s2 = b
    row = (s1 - 0x81) * 2 + 1 if s1 < 0xA0 else (s1 - 0xC1) * 2 + 1
    if s2 >= 0x9F:
        row += 1
        col = s2 - 0x9E
    else:
        col = s2 - 0x3F - (1 if s2 >= 0x80 else 0)
    return 158 + (row - 1) * 94 + (col - 1)
