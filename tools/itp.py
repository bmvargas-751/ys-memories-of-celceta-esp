"""Imágenes ITP de Celceta (versión 2, con banderas): leer y escribir.

Formato según Cradle (Aureole Suite, https://github.com/Aureole-Suite/Cradle,
cradle/src/itp/read.rs). Las variantes que usa el texto de Celceta:

    0x40108810  32 bits BGRA, sin compresión, lineal:
                u32 banderas, u32 ancho, u32 alto, píxeles
    0x50111001  256 colores, FALCOM3 en un bloque, mosaicos de 32×32
    0x50131001  256 colores, FALCOM3 en bloques de 0x40000, mosaicos de 32×32
                u32 banderas, u32 ancho, u32 alto, u32 colores,
                paleta (FALCOM3, BGRA), índices (FALCOM3)

Los mosaicos se guardan en orden de filas de mosaico; dentro de cada uno, por
filas. to_rgba() da los píxeles en orden lineal y from_rgba() vuelve al
formato del archivo (con la paleta original si alcanza, si no una nueva).
"""
import struct

import falcom

RAW32 = 0x40108810
IDX_BZ1 = 0x50111001
IDX_BZ2 = 0x50131001
TILE = 32
BZ2_BLOCK = 0x40000


def _untile(data, w, h):
    out = bytearray(w * h)
    k = 0
    for ty in range(h // TILE):
        for tx in range(w // TILE):
            for y in range(TILE):
                row = (ty * TILE + y) * w + tx * TILE
                out[row:row + TILE] = data[k:k + TILE]
                k += TILE
    return bytes(out)


def _tile(data, w, h):
    out = bytearray()
    for ty in range(h // TILE):
        for tx in range(w // TILE):
            for y in range(TILE):
                row = (ty * TILE + y) * w + tx * TILE
                out += data[row:row + TILE]
    return bytes(out)


class ITP:
    def __init__(self, data):
        self.data = data
        self.flags, self.w, self.h = struct.unpack_from("<III", data, 0)
        if self.flags == RAW32:
            if len(data) != 12 + self.w * self.h * 4:
                raise ValueError("tamaño raro")
            self.palette = None
            self.pixels = data[12:]           # BGRA lineal
        elif self.flags in (IDX_BZ1, IDX_BZ2):
            n = struct.unpack_from("<I", data, 12)[0]
            p = 16
            pal, used = falcom.decompress_falcom3(data[p:])
            p += used
            self.palette = [pal[i * 4:i * 4 + 4] for i in range(n)]   # BGRA
            idx = bytearray()
            while len(idx) < self.w * self.h:
                out, used = falcom.decompress_falcom3(data[p:])
                idx += out
                p += used
                if self.flags == IDX_BZ1:
                    break
            if len(idx) != self.w * self.h or p != len(data):
                raise ValueError("índices de largo raro")
            self.pixels = _untile(bytes(idx), self.w, self.h)   # índices lineales
        else:
            raise ValueError(f"variante ITP no soportada: {self.flags:#x}")

    def to_rgba(self):
        """Bytes RGBA lineales (para PIL)."""
        if self.flags == RAW32:
            px = self.pixels
            out = bytearray(len(px))
            out[0::4], out[1::4], out[2::4], out[3::4] = px[2::4], px[1::4], px[0::4], px[3::4]
            return bytes(out)
        lut = [bytes([c[2], c[1], c[0], c[3]]) for c in self.palette]
        lut += [b"\0\0\0\0"] * (256 - len(lut))
        return b"".join(lut[i] for i in self.pixels)

    def from_rgba(self, rgba):
        """Reemplaza la imagen con píxeles RGBA lineales del mismo tamaño."""
        if len(rgba) != self.w * self.h * 4:
            raise ValueError("la imagen nueva tiene otro tamaño")
        if self.flags == RAW32:
            out = bytearray(len(rgba))
            out[0::4], out[1::4], out[2::4], out[3::4] = rgba[2::4], rgba[1::4], rgba[0::4], rgba[3::4]
            self.pixels = bytes(out)
            return
        from PIL import Image
        quads = [rgba[i:i + 4] for i in range(0, len(rgba), 4)]
        # 1) cada color al más cercano de la paleta original (que ya trae los
        #    degradados del texto); 2) una paleta nueva de 256 colores. Se
        #    queda la que se aleje menos de la imagen editada.
        pal_rgba = [bytes([c[2], c[1], c[0], c[3]]) for c in self.palette]
        exact = {q: i for i, q in enumerate(pal_rgba)}
        near = {}
        for q in set(quads):
            if q in exact:
                near[q] = exact[q]
            else:
                near[q] = min(range(len(pal_rgba)),
                              key=lambda i: sum((a - b) ** 2 for a, b in zip(q, pal_rgba[i])))
        px1 = bytes(near[q] for q in quads)
        err1 = sum(sum((a - b) ** 2 for a, b in zip(q, pal_rgba[near[q]])) for q in quads)
        if err1 == 0:
            self.pixels = px1
            return
        im = Image.frombytes("RGBA", (self.w, self.h), rgba)
        q2 = im.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
        pal = q2.getpalette(rawmode="RGBA")[:256 * 4]
        pal += [0] * (256 * 4 - len(pal))
        pal2 = [bytes(pal[i * 4:i * 4 + 4]) for i in range(256)]
        px2 = q2.tobytes()
        err2 = sum(sum((a - b) ** 2 for a, b in zip(q, pal2[k])) for q, k in zip(quads, px2))
        if err1 <= err2:
            self.pixels = px1
        else:
            self.palette = [bytes([c[2], c[1], c[0], c[3]]) for c in pal2]
            self.pixels = px2

    def build(self):
        if self.flags == RAW32:
            return struct.pack("<III", self.flags, self.w, self.h) + self.pixels
        out = bytearray(struct.pack("<IIII", self.flags, self.w, self.h, len(self.palette)))
        out += falcom.compress_falcom3(b"".join(self.palette))
        idx = _tile(self.pixels, self.w, self.h)
        if self.flags == IDX_BZ1:
            out += falcom.compress_falcom3(idx)
        else:
            for i in range(0, len(idx), BZ2_BLOCK):
                out += falcom.compress_falcom3(idx[i:i + BZ2_BLOCK])
        return bytes(out)
