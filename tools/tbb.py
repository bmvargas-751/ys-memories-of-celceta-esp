"""Tablas TBB planas de Celceta (lang/*/text/*.tbb): leer y reconstruir.

Formato (el mismo de Ys VIII; ver tbbconv.js de yosh778/YsVIII-tools):
u32 columnas, u32 filas, u32 largo del bloque de cadenas; las cadenas
terminadas en NUL; y una tabla de u32 (filas × columnas) con el offset de cada
celda dentro del bloque.

Varias celdas pueden compartir el mismo offset (cadenas repetidas o vacías).
Para que la ida y vuelta sea idéntica, build() conserva el bloque y los
offsets originales mientras no cambie nada, y si cambia algo escribe las
cadenas en el orden de su primera aparición en el bloque, reutilizando las
iguales.
"""
import struct


class TBB:
    def __init__(self, data):
        self.cols, self.rows, ln = struct.unpack_from("<III", data, 0)
        if 12 + ln + self.cols * self.rows * 4 != len(data):
            raise ValueError("no es un TBB plano")
        self.block = data[12:12 + ln]
        self.offs = list(struct.unpack_from(f"<{self.cols * self.rows}I", data, 12 + ln))
        self.cells = [self._at(o) for o in self.offs]
        self._orig = list(self.cells)
        self._data = data

    def _at(self, o):
        end = self.block.index(b"\0", o)
        return self.block[o:end]

    def get(self, r, c):
        return self.cells[r * self.cols + c]

    def set(self, r, c, value):
        self.cells[r * self.cols + c] = value

    def row_list(self):
        return [self.cells[r * self.cols:(r + 1) * self.cols] for r in range(self.rows)]

    def set_rows(self, rows):
        """Reemplaza todas las filas (pueden ser más o menos que antes)."""
        assert all(len(r) == self.cols for r in rows)
        self.rows = len(rows)
        self.cells = [v for r in rows for v in r]

    def build(self):
        if self.cells == self._orig:
            return self._data
        block = bytearray()
        where = {}
        offs = []
        for v in self.cells:
            if v not in where:
                where[v] = len(block)
                block += v + b"\0"
            offs.append(where[v])
        head = struct.pack("<III", self.cols, self.rows, len(block))
        return head + bytes(block) + struct.pack(f"<{len(offs)}I", *offs)
