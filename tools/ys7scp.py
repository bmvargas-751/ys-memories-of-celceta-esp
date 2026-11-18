"""Guiones YS7_SCP de Celceta (lang/*/script/*.bin): leer y reconstruir.

Formato (el mismo de Ys VIII; ver bin2script.cpp de yosh778/YsVIII-tools):
- Cabecera: "YS7_SCP\\0", 3 bytes reservados, u8 versión, u64 suma (el juego
  no la comprueba), u32 número de segmentos.
- Por segmento: nombre de 0x20 bytes, u32 tamaño, u32 offset desde el inicio.
- Cada segmento es una lista de instrucciones: u16 opcode (0x8000 en adelante)
  y sus argumentos, cada uno con su etiqueta u16:
    0x82DD entero i32 · 0x82DE real f32 · 0x82DF cadena (u32 largo + bytes)
    0x82E0 expresión (u32 largo + bytes)
- Los saltos (if, elseIf, else, while, break, case, default, Execute, 0x8085)
  llevan como último entero un offset relativo al final de ese argumento.

Al reconstruir se recalculan los saltos, el tamaño y el offset de cada segmento,
así que las cadenas pueden cambiar de largo.
"""
import struct

INT, FLOAT, STR, EXPR = 0x82DD, 0x82DE, 0x82DF, 0x82E0
ARG_TAGS = (INT, FLOAT, STR, EXPR)
JUMPS = {0x8080, 0x8081, 0x8082, 0x8084, 0x8085, 0x8086, 0x8088, 0x8089, 0x804E}


class Instr:
    __slots__ = ("op", "args", "target")

    def __init__(self, op, args):
        self.op = op
        self.args = args      # lista de (etiqueta, valor): int, float crudo (bytes) o bytes
        self.target = None    # índice de la instrucción de destino si es un salto


def _parse_segment(seg):
    p, n = 0, len(seg)
    instrs, starts = [], []
    while p < n:
        if n - p < 2:
            raise ValueError(f"segmento: sobran {n - p} bytes en {p:#x}")
        op = struct.unpack_from("<H", seg, p)[0]
        if op in ARG_TAGS or op < 0x8000:
            raise ValueError(f"opcode raro {op:#06x} en {p:#x}")
        starts.append(p)
        p += 2
        args = []
        while p + 2 <= n:
            tag = struct.unpack_from("<H", seg, p)[0]
            if tag not in ARG_TAGS:
                break
            if tag == INT:
                args.append((tag, struct.unpack_from("<i", seg, p + 2)[0]))
                p += 6
            elif tag == FLOAT:
                args.append((tag, bytes(seg[p + 2:p + 6])))
                p += 6
            else:
                ln = struct.unpack_from("<I", seg, p + 2)[0]
                args.append((tag, bytes(seg[p + 6:p + 6 + ln])))
                p += 6 + ln
                if p > n:
                    raise ValueError(f"argumento fuera del segmento en {p:#x}")
        instrs.append(Instr(op, args))
    ends = starts[1:] + [n]
    pos2idx = {s: i for i, s in enumerate(starts)}
    pos2idx[n] = len(instrs)
    for i, ins in enumerate(instrs):
        if ins.op in JUMPS and ins.args and ins.args[-1][0] == INT:
            dest = ends[i] + ins.args[-1][1]
            if dest not in pos2idx:
                raise ValueError(f"salto a {dest:#x} que no es una instrucción (desde {starts[i]:#x})")
            ins.target = pos2idx[dest]
    return instrs


def _arg_bytes(tag, val):
    if tag == INT:
        return struct.pack("<Hi", tag, val)
    if tag == FLOAT:
        return struct.pack("<H", tag) + val
    return struct.pack("<HI", tag, len(val)) + val


def _instr_size(ins):
    return 2 + sum(6 if t in (INT, FLOAT) else 6 + len(v) for t, v in ins.args)


def _build_segment(instrs):
    starts, p = [], 0
    for ins in instrs:
        starts.append(p)
        p += _instr_size(ins)
    total = p
    ends = starts[1:] + [total]
    allpos = starts + [total]
    out = bytearray()
    for i, ins in enumerate(instrs):
        args = ins.args
        if ins.target is not None:
            args = args[:-1] + [(INT, allpos[ins.target] - ends[i])]
        out += struct.pack("<H", ins.op)
        for t, v in args:
            out += _arg_bytes(t, v)
    return bytes(out)


class Script:
    def __init__(self, data):
        if data[:8] != b"YS7_SCP\0":
            raise ValueError("no es YS7_SCP")
        self.head = data[:0x14]           # magia, reservado, versión, suma
        nseg = struct.unpack_from("<I", data, 0x14)[0]
        self.names, self.segments = [], []
        raw = []
        for i in range(nseg):
            o = 0x18 + i * 0x28
            name = data[o:o + 0x20]
            size, off = struct.unpack_from("<II", data, o + 0x20)
            raw.append((off, size))
            self.names.append(name)
        # El orden de los datos en el archivo es el de la tabla y sin huecos;
        # se comprueba para poder reconstruir igual.
        p = 0x18 + nseg * 0x28
        for off, size in raw:
            if off != p:
                raise ValueError(f"segmento en {off:#x}, se esperaba {p:#x}")
            p += size
        self.tail = data[p:]
        for off, size in raw:
            self.segments.append(_parse_segment(data[off:off + size]))

    def build(self):
        segs = [_build_segment(s) for s in self.segments]
        out = bytearray(self.head)
        out += struct.pack("<I", len(segs))
        p = 0x18 + len(segs) * 0x28
        for name, seg in zip(self.names, segs):
            out += name + struct.pack("<II", len(seg), p)
            p += len(seg)
        for seg in segs:
            out += seg
        out += self.tail
        return bytes(out)

    def strings(self):
        """(segmento, instrucción, argumento, bytes) de cada cadena."""
        for si, seg in enumerate(self.segments):
            for ii, ins in enumerate(seg):
                for ai, (t, v) in enumerate(ins.args):
                    if t == STR:
                        yield si, ii, ai, v

    def set_string(self, si, ii, ai, value):
        ins = self.segments[si][ii]
        assert ins.args[ai][0] == STR
        ins.args[ai] = (STR, value)

    def seg_name(self, si):
        return self.names[si].split(b"\0", 1)[0].decode("ascii")
