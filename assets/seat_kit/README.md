# Seat kit

Modular seat parts used by the Light Spill Lab default room. Every part is instanced (one copy in memory, one draw call per mesh).

| File | What | Instances |
|---|---|---|
| `seat.glb` / `seat.obj` | Cushion + backrest | 252 |
| `armrest.glb` / `armrest.obj` | Armrest top + leg (shared between neighbour seats) | 288 |
| `row_reference.glb` | 3 seats + 4 armrests at the real spacing, for context only (not loaded by the app) | - |

## Conventions

- Units: meters. Y up, front of the seat facing **-Z** (glTF). In Blender that means the seat faces **+Y** (the glTF exporter converts).
- Origin: on the floor, centered under the part.
- Seat pitch: 0.6 m (seat centers). Armrests sit between seats at +-0.3 m from each seat center.
- Material names drive the highlight: names with `fabric/cloth/velvet/cushion/seat` get a soft sheen, `plastic/arm/metal/wood/leg` a tighter highlight.

## Workflow

1. Import `seat.glb` and `armrest.glb` in Blender (or `row_reference.glb` to see the spacing).
2. Improve, keep the origin and orientation, export as GLB with the **same file names** into this folder.
3. Commit and push. The app loads `assets/seat_kit/seat.glb` and `armrest.glb` at startup; a missing file falls back to the built-in part.
4. For quick tests without pushing, use **Load seat GLB / Load armrest GLB** in the app.

Budget tip for Quest: aim for 300 to 600 triangles per seat and bake the bevel detail into a normal map.
