# Cinema room model

Export of the built-in cinema room, in the app's real scale. Open it in Blender (File > Import > glTF 2.0), texture / remodel it, export it back as **`cinema_custom.glb`** in this folder. The app (Light Spill Lab v0.16.5+) loads it automatically and uses it instead of the built-in look.

| File | What it is |
|---|---|
| `cinema_room.glb` | The room shell: walls, floor, steps, ceiling, stage, screen frame, EXIT door and sign. No seats. |
| `cinema_room_with_seats.glb` | Same plus every seat and armrest, as a reference for context (don't export these back). |
| `cinema_custom.glb` | **Your version.** The app picks it up from here. |

## Rules (only these)

- **Don't move the origin or the floor.** Units are meters, Y up (Blender converts to Z up on import and back on export, keep the glTF exporter default "+Y Up").
- Origin: floor level, center line of the room. The screen center is at (0, 4.6, -10.89) in glTF coordinates, 12 x 6.75 m, curved 25 deg.
- The seats are placed by the app (seat kit in `assets/seat_kit/`), on the same spots as in `cinema_room_with_seats.glb`. Keep the floor / steps where they are so the seats still sit on them.

## Everything else is free

- **Names don't matter.** One mesh or a hundred, any names, any hierarchy.
- Optional: a mesh named `Screen...` is hidden (the app draws the video screen itself).
- Materials: Principled BSDF (base color, roughness, normal map) exports fine. The screen light (light spill) is added on top of every material automatically. Baked AO / lighting in the base color works well too.
- Keep it light for the Quest: aim for under ~100k triangles and textures of 2K or less.

## In the app

- Menu > **Room model**: switch between your model and the built-in one.
- Desktop: **Load room model (keep seats)...** tests a GLB from your disk without copying it here.

Marcelo Souza / Kumodot.art - 2026 // @Msouza3d - [Support Marcelo Souza](https://ko-fi.com/msouza3d)
