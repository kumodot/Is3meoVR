"""
Seat Kit Splitter v1.0.1 - SilVRCine
Marcelo Souza / Kumodot.art - 2026 // @Msouza3d
Support Marcelo Souza: https://ko-fi.com/msouza3d

Takes one GLB with the seat AND the armrest (e.g. a Substance Painter export, parts moved apart
for baking) and writes the two files the app loads: seat_ms.glb + armrest_ms.glb.
Parts are told apart by name: anything with "arm" in its node/mesh name is the armrest.
Each part is moved back to where the current seat_ms.glb / armrest_ms.glb sit (same bounding box
center in X/Z, same floor height). With no reference file: centered in X/Z, standing on the floor.
The previous files are kept as *_prev.glb. Textures and materials are copied as they are.

Usage: drag the GLB onto split_seat_kit.bat, or: python split_seat_kit_v1.0.1.py painter_export.glb
"""
import json
import math
import shutil
import struct
import sys
from pathlib import Path

VERSION = '1.0.1'
HERE = Path(__file__).resolve().parent
OUT = {'seat': HERE / 'seat_ms.glb', 'arm': HERE / 'armrest_ms.glb'}


def read_glb(path):
    b = Path(path).read_bytes()
    if b[:4] != b'glTF':
        raise SystemExit(f'{path} is not a binary GLB')
    jl = struct.unpack('<I', b[12:16])[0]
    j = json.loads(b[20:20 + jl])
    binc = b''
    off = 20 + jl
    if off < len(b):
        bl = struct.unpack('<I', b[off:off + 4])[0]
        binc = b[off + 8:off + 8 + bl]
    return j, binc


def write_glb(path, j, binc):
    js = json.dumps(j, separators=(',', ':')).encode('utf-8')
    js += b' ' * ((4 - len(js) % 4) % 4)
    binc += b'\0' * ((4 - len(binc) % 4) % 4)
    total = 12 + 8 + len(js) + (8 + len(binc) if binc else 0)
    out = struct.pack('<4sII', b'glTF', 2, total) + struct.pack('<I4s', len(js), b'JSON') + js
    if binc:
        out += struct.pack('<I4s', len(binc), b'BIN\0') + binc
    Path(path).write_bytes(out)


# ---- 4x4 matrices, column-major like glTF ----
def mat_mul(a, b):
    return [sum(a[k * 4 + r] * b[c * 4 + k] for k in range(4)) for c in range(4) for r in range(4)]


def node_matrix(n):
    if 'matrix' in n:
        return list(n['matrix'])
    tx, ty, tz = n.get('translation', [0, 0, 0])
    x, y, z, w = n.get('rotation', [0, 0, 0, 1])
    sx, sy, sz = n.get('scale', [1, 1, 1])
    r = [1 - 2 * (y * y + z * z), 2 * (x * y + z * w), 2 * (x * z - y * w),
         2 * (x * y - z * w), 1 - 2 * (x * x + z * z), 2 * (y * z + x * w),
         2 * (x * z + y * w), 2 * (y * z - x * w), 1 - 2 * (x * x + y * y)]
    return [r[0] * sx, r[1] * sx, r[2] * sx, 0, r[3] * sy, r[4] * sy, r[5] * sy, 0,
            r[6] * sz, r[7] * sz, r[8] * sz, 0, tx, ty, tz, 1]


def mesh_nodes(j):
    """[(node index, world matrix, names along the path)] for every node with a mesh in the scene."""
    out = []
    scene = j['scenes'][j.get('scene', 0)]

    def walk(i, parent, names):
        n = j['nodes'][i]
        m = mat_mul(parent, node_matrix(n))
        nm = names + [n.get('name', '')]
        if 'mesh' in n:
            out.append((i, m, nm + [j['meshes'][n['mesh']].get('name', '')]))
        for c in n.get('children', []):
            walk(c, m, nm)
    ident = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    for i in scene['nodes']:
        walk(i, ident, [])
    return out


def bbox(j, items):
    lo, hi = [math.inf] * 3, [-math.inf] * 3
    for i, m, _ in items:
        for p in j['meshes'][j['nodes'][i]['mesh']]['primitives']:
            a = j['accessors'][p['attributes']['POSITION']]
            for cx in (a['min'][0], a['max'][0]):
                for cy in (a['min'][1], a['max'][1]):
                    for cz in (a['min'][2], a['max'][2]):
                        w = [m[0] * cx + m[4] * cy + m[8] * cz + m[12], m[1] * cx + m[5] * cy + m[9] * cz + m[13],
                             m[2] * cx + m[6] * cy + m[10] * cz + m[14]]
                        lo = [min(lo[k], w[k]) for k in range(3)]
                        hi = [max(hi[k], w[k]) for k in range(3)]
    return lo, hi


def anchor(lo, hi):
    # what has to match: center in X and Z, floor (lowest point) in Y
    return [(lo[0] + hi[0]) / 2, lo[1], (lo[2] + hi[2]) / 2]


def main():
    print(f'Seat Kit Splitter v{VERSION} - Marcelo Souza / Kumodot.art - 2026 // @Msouza3d')
    args = [a for a in sys.argv[1:] if a.strip()]
    if not args or not Path(args[0]).is_file():
        print('No file given. Drag the Painter GLB (seat + armrest) onto split_seat_kit.bat (double-clicking it does nothing).')
        return
    src = Path(args[0])
    j, binc = read_glb(src)
    items = mesh_nodes(j)
    parts = {'seat': [], 'arm': []}
    for it in items:
        parts['arm' if any('arm' in s.lower() for s in it[2]) else 'seat'].append(it)
    for key, its in parts.items():
        if not its:
            print(f'No {key} meshes found (armrest = a name with "arm" in it). Skipped.')
            continue
        cur = anchor(*bbox(j, its))
        ref_file = OUT[key]
        target = [0.0, 0.0, 0.0]
        if ref_file.exists():
            rj, _ = read_glb(ref_file)
            target = anchor(*bbox(rj, mesh_nodes(rj)))
        off = [target[k] - cur[k] for k in range(3)]
        nj = json.loads(json.dumps(j))
        new_children = []
        for i, m, _ in its:
            nj['nodes'].append({'name': j['nodes'][i].get('name', key), 'mesh': j['nodes'][i]['mesh'], 'matrix': m})
            new_children.append(len(nj['nodes']) - 1)
        nj['nodes'].append({'name': 'Seat' if key == 'seat' else 'Armrest', 'translation': off, 'children': new_children})
        nj['scenes'] = [{'nodes': [len(nj['nodes']) - 1]}]
        nj['scene'] = 0
        if ref_file.exists():
            shutil.copy2(ref_file, ref_file.with_name(ref_file.stem + '_prev.glb'))
        write_glb(ref_file, nj, binc)
        print(f'{ref_file.name}: {len(its)} mesh(es), moved by ({off[0]:+.3f}, {off[1]:+.3f}, {off[2]:+.3f}) m')
    print('Done. Reload SilVRCine to see them.')


if __name__ == '__main__':
    main()
