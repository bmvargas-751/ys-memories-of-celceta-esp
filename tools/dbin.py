"""Textos de la interfaz de Celceta (lang/en/text/strSystem.dbin).

Formato (una tabla de 690 filas × 2 columnas de cadenas):
- 690 filas de 8 bytes: u32 offset del ID y u32 offset del texto, contados
  desde el inicio del bloque de cadenas.
- 2 descriptores de columna de 16 bytes (en 0x1590).
- Bloque de cadenas (en 0x15B0) terminadas en NUL, sin repetir, en el orden en
  que aparecen por primera vez en la tabla.
- Ceros hasta un múltiplo de 16.
- Pie de 64 bytes que empieza con «STRL»: filas (690), dónde están los
  descriptores (0x1590) y las cadenas (0x15B0), y cuántas cadenas distintas hay.
  Ese número hay que actualizarlo si cambia.

build() devuelve los bytes originales si no cambió nada.
"""
import struct

ROWS = 690
NOFFS = ROWS * 2
FOOTER = 64
COUNT_AT = 40     # offset dentro del pie del número de cadenas distintas


class DBIN:
    def __init__(self, data):
        self.data = data
        foot = len(data) - FOOTER
        if data[foot:foot + 4] != b"STRL":
            raise ValueError("falta el pie STRL")
        self.footer = data[foot:]
        rows, rowsize, cols_at, ncols, pool_at, count = struct.unpack_from("<IIIIII", self.footer, 20)
        if rows != ROWS or rowsize != 8 or cols_at != NOFFS * 4 or pool_at != cols_at + 16 * ncols:
            raise ValueError("pie STRL inesperado")
        if struct.unpack_from("<I", self.footer, COUNT_AT)[0] != count:
            raise ValueError("pie STRL: posición del conteo")
        self.head = data[:pool_at]          # tabla + descriptores (los offsets se rehacen)
        self.pool_at = pool_at
        offs = struct.unpack_from(f"<{NOFFS}I", data, 0)
        self.values = [data[pool_at + o:data.index(b"\0", pool_at + o)] for o in offs]
        if len(set(self.values)) != count:
            raise ValueError("el número de cadenas no coincide con el pie")
        self._orig = list(self.values)

    def pairs(self):
        return [(self.values[i], self.values[i + 1]) for i in range(0, NOFFS, 2)]

    def set_text(self, i, value):
        self.values[2 * i + 1] = value

    def build(self, force=False):
        if self.values == self._orig and not force:
            return self.data
        pool = bytearray()
        where = {}
        for v in self.values:            # orden de primera aparición, sin repetir
            if v not in where:
                where[v] = len(pool)
                pool += v + b"\0"
        end = self.pool_at + len(pool)
        pool += b"\0" * (-end % 16)
        footer = bytearray(self.footer)
        struct.pack_into("<I", footer, COUNT_AT, len(where))
        offs = struct.pack(f"<{NOFFS}I", *(where[v] for v in self.values))
        return offs + self.head[NOFFS * 4:] + bytes(pool) + bytes(footer)
