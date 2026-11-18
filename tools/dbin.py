"""Textos de la interfaz de Celceta (lang/en/text/strSystem.dbin).

Formato: 1380 offsets u32 (690 pares ID / texto), 32 bytes de otros datos y el
bloque de cadenas terminadas en NUL; los offsets cuentan desde el inicio del
bloque y pueden repetirse (cadenas compartidas). Al final del bloque hay
cadenas que ningún offset usa: se conservan.

build() devuelve los bytes originales si no cambió nada; si cambió algo, vuelve
a escribir el bloque con las cadenas en el orden original, reutilizando las
iguales.
"""
import struct

NOFFS = 1380
MIDDLE = 32


class DBIN:
    def __init__(self, data):
        self.data = data
        self.offs = list(struct.unpack_from(f"<{NOFFS}I", data, 0))
        self.middle = data[4 * NOFFS:4 * NOFFS + MIDDLE]
        self.base = 4 * NOFFS + MIDDLE
        block = data[self.base:]
        # todas las cadenas del bloque, en orden, con su offset
        self.blocks = []
        p = 0
        while p < len(block):
            e = block.index(b"\0", p)
            self.blocks.append((p, block[p:e]))
            p = e + 1
        self.tail = block[p:]
        at = {o: s for o, s in self.blocks}
        for o in self.offs:
            if o not in at:
                raise ValueError(f"offset {o} no es el inicio de una cadena")
        self.values = [at[o] for o in self.offs]
        self._orig = list(self.values)

    def pairs(self):
        return [(self.values[i], self.values[i + 1]) for i in range(0, NOFFS, 2)]

    def set_text(self, i, value):
        self.values[2 * i + 1] = value

    def build(self):
        if self.values == self._orig:
            return self.data
        # orden: las cadenas originales en su orden, cambiadas donde toca
        out = bytearray()
        where = {}
        order = []
        seen = set()
        refs = set(self.offs)
        for p, s in self.blocks:
            if p in refs:
                continue
            order.append(s)  # sin referencia: se conserva
        used = []
        for v in self.values:
            if v not in seen:
                seen.add(v)
                used.append(v)
        for s in used + [s for s in order if s not in seen]:
            if s not in where:
                where[s] = len(out)
                out += s + b"\0"
        offs = [where[v] for v in self.values]
        return struct.pack(f"<{NOFFS}I", *offs) + self.middle + bytes(out) + self.tail
