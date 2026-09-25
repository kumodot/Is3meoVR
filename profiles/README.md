# Player profiles

Each JSON maps the cinema's MEDIA-mode actions to keyboard shortcuts of a PC player. The Light Spill Lab (v0.8.0+) loads every id listed in `index.json`; pick one in the VR menu under **Player profile**.

```json
{
  "id": "stremio",
  "name": "Stremio",
  "app": "stremio",
  "actions": {
    "playPause": { "key": "Space", "label": "Play/Pause" },
    "seekFwdSmall": { "key": "ArrowRight", "mods": ["Shift"], "label": "+10s" }
  }
}
```

- `app`: id the Is3meo Bridge opens with **PC: open player app** (see `apps` in the Bridge config).
- `key`: `Space`, `Enter`, `Escape`, `Backspace`, `Tab`, `ArrowLeft/Right/Up/Down`, `PageUp/PageDown`, `Home/End`, `KeyA`..`KeyZ`, `Digit0`..`Digit9`, `F1`..`F12`, `Equal`, `Minus`, `Comma`, `Period`, `MediaPlayPause`, `MediaNextTrack`, `MediaPrevTrack`, `VolumeUp/Down/Mute`.
- `mods`: any of `Shift`, `Control`, `Alt`.
- `label`: text shown on the controller hints. Use `null` for actions the player does not have.

Actions: `playPause`, `seekBack`, `seekFwd`, `seekBackSmall`, `seekFwdSmall`, `volUp`, `volDown`, `mute`, `fullscreen`, `back`, `showUI`, `next`, `subSizeUp`, `subSizeDown`, `subDelayUp`, `subDelayDown`.

New profile: add `myplayer.json`, add `"myplayer"` to `index.json`, push. PotPlayer and VLC mappings are defaults from memory; tweak them if your hotkeys differ.

Marcelo Souza / Kumodot.art - 2026 // @Msouza3d - [Support Marcelo Souza](https://ko-fi.com/msouza3d)
