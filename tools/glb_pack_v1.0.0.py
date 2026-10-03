"""
GLB Pack v1.0.0 - SilVRCine
Marcelo Souza / Kumodot.art - 2026 // @Msouza3d
Support Marcelo Souza: https://ko-fi.com/msouza3d

Makes a model light for the Quest: one .glb with every texture embedded as JPEG.
- Input: a .glb (textures inside) or a .gltf (+ .bin + PNG files next to it, like Substance Painter exports).
- PNG textures become JPEG (quality 90, normal maps 95). Textures with real transparency stay PNG.
- Textures bigger than 2048 px are scaled down to 2048.
- Output: <name>.glb next to the input. An existing file with that name is kept as <name>_prev.glb.

Usage: drag the .glb / .gltf onto glb_pack.bat, or: python glb_pack_v1.0.0.py model.gltf
Needs Pillow (pip install pillow).
"""
import base64
import io
import json
import shutil
import struct
import sys
from pathlib import Path

VERSION = '1.0.0'
MAX_SIZE = 2048
JPEG_QUALITY = 90
JPEG_QUALITY_NORMAL = 95


def load(path):
    path = Path(path)
    if path.suffix.lower() == '.glb':
        b = path.read_bytes()
        if b[:4] != b'glTF':
            raise SystemExit(f'{path.name} is not a binary GLB')
        jl = struct.unpack('<I', b[12:16])[0]
        j = json.loads(b[20:20 + jl])
        off = 20 + jl
        binc = b''
        if off < len(b):
            bl = struct.unpack('<I', b[off:off + 4])[0]
            binc = b[off + 8:off + 8 + bl]
        buffers = [binc]
        for extra in j.get('buffers', [])[1:]:
            buffers.append(read_uri(path.parent, extra.get('uri', '')))
        return j, buffers
    j = json.loads(path.read_text(encoding='utf-8'))
    buffers = [read_uri(path.parent, buf.get('uri', '')) for buf in j.get('buffers', [])]
    return j, buffers


def read_uri(folder, uri):
    if uri.startswith('data:'):
        return base64.b64decode(uri.split(',', 1)[1])
    from urllib.parse import unquote
    return (folder / unquote(uri)).read_bytes()


def view_bytes(j, buffers, vi):
    v = j['bufferViews'][vi]
    o = v.get('byteOffset', 0)
    return buffers[v['buffer']][o:o + v['byteLength']]


def convert(data, normal):
    from PIL import Image
    im = Image.open(io.BytesIO(data))
    w, h = im.size
    if max(w, h) > MAX_SIZE:
        s = MAX_SIZE / max(w, h)
        im = im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    if im.mode in ('RGBA', 'LA', 'P'):
        rgba = im.convert('RGBA')
        if rgba.getextrema()[3][0] < 255:  # real transparency: keep PNG
            out = io.BytesIO()
            rgba.save(out, 'PNG', optimize=True)
            return out.getvalue(), 'image/png', im.size
        im = rgba.convert('RGB')
    elif im.mode != 'RGB':
        im = im.convert('RGB')
    out = io.BytesIO()
    im.save(out, 'JPEG', quality=JPEG_QUALITY_NORMAL if normal else JPEG_QUALITY, optimize=True, subsampling=0 if normal else 2)
    return out.getvalue(), 'image/jpeg', im.size


def main():
    print(f'GLB Pack v{VERSION} - Marcelo Souza / Kumodot.art - 2026 // @Msouza3d')
    if len(sys.argv) < 2:
        print('Drag a .glb or .gltf onto glb_pack.bat')
        return
    src = Path(sys.argv[1])
    j, buffers = load(src)
    size_in = src.stat().st_size
    if src.suffix.lower() == '.gltf':
        size_in += sum(len(b) for b in buffers)
        size_in += sum(len(read_uri(src.parent, im['uri'])) for im in j.get('images', []) if 'uri' in im)

    normal_images = set()
    for m in j.get('materials', []):
        t = m.get('normalTexture')
        if t is not None:
            normal_images.add(j['textures'][t['index']].get('source'))

    image_views = {img['bufferView'] for img in j.get('images', []) if 'bufferView' in img}
    # 1. new image bytes
    new_images = []
    for i, img in enumerate(j.get('images', [])):
        data = view_bytes(j, buffers, img['bufferView']) if 'bufferView' in img else read_uri(src.parent, img['uri'])
        try:
            data2, mime, wh = convert(data, i in normal_images)
            print(f"  texture {i} {img.get('name', '')}: {len(data) // 1024} KB -> {len(data2) // 1024} KB {mime.split('/')[1].upper()} {wh[0]}x{wh[1]}")
        except Exception as e:
            print(f'  texture {i}: kept as is ({e})')
            data2, mime = data, img.get('mimeType', 'image/png')
        new_images.append((data2, mime))

    # 2. one new buffer: geometry views first (same indices), then the images
    blob = bytearray()

    def add(data):
        while len(blob) % 4:
            blob.append(0)
        o = len(blob)
        blob.extend(data)
        return o

    views = []
    for vi, v in enumerate(j.get('bufferViews', [])):
        nv = dict(v)
        if vi in image_views:
            views.append(None)  # replaced below
            continue
        nv['byteOffset'] = add(view_bytes(j, buffers, vi))
        nv['buffer'] = 0
        views.append(nv)
    for i, img in enumerate(j.get('images', [])):
        data2, mime = new_images[i]
        o = add(data2)
        nv = {'buffer': 0, 'byteOffset': o, 'byteLength': len(data2)}
        if 'bufferView' in img and views[img['bufferView']] is None:
            views[img['bufferView']] = nv
        else:
            views.append(nv)
            img['bufferView'] = len(views) - 1
        img.pop('uri', None)
        img['mimeType'] = mime
    # an image view shared by two images would stay None: drop nothing, just keep it empty-safe
    views = [v if v is not None else {'buffer': 0, 'byteOffset': 0, 'byteLength': 0} for v in views]
    j['bufferViews'] = views
    while len(blob) % 4:
        blob.append(0)
    j['buffers'] = [{'byteLength': len(blob)}]

    js = json.dumps(j, separators=(',', ':')).encode('utf-8')
    js += b' ' * ((4 - len(js) % 4) % 4)
    out = struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(js) + 8 + len(blob))
    out += struct.pack('<I4s', len(js), b'JSON') + js + struct.pack('<I4s', len(blob), b'BIN\0') + bytes(blob)

    dst = src.with_suffix('.glb')
    if dst.exists():
        shutil.copy2(dst, dst.with_name(dst.stem + '_prev.glb'))
    dst.write_bytes(out)
    print(f'{dst.name}: {size_in / 1048576:.1f} MB -> {len(out) / 1048576:.1f} MB')


if __name__ == '__main__':
    main()
