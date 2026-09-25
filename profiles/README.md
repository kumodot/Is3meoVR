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

## Button mappings (profile v2, Light Spill Lab v0.13.0+)

The easy way: the **Button Mapping** tab in the Is3meo Bridge. Pick an app, click the buttons on the drawing, type the label and press the shortcut. It saves `bridge/profiles_user/<id>.json`, which overrides the default profile with the same id, and sends it to the Quest.

A v2 profile adds `buttons.media` with one map per layer (`base`, `altL` = left grip held, `altR` = right grip held):

```json
"buttons": { "media": {
  "base": {
    "R.a": { "type": "key", "key": "Space", "label": "Play/Pause" },
    "R.b": { "type": "key", "key": "ArrowRight", "mods": ["Control"], "label": "Skip intro" },
    "L.trigger": { "type": "openApp" }
  },
  "altL": {}, "altR": {}
} }
```

- Slots: `L.trigger`, `L.left/right/up/down` (left stick), `R.a`, `R.b`, `R.trigger`, `R.left/right/up/down` (right stick). X, Y, grips and stick clicks are global.
- `type`: `key`, `openApp` (opens the app picked on the Quest) or `none`.
- `mods` also accepts `Meta` (Windows key). More keys: `Numpad0`..`Numpad9`, `NumpadAdd` etc., `Backslash`, `PrintScreen`, `Pause`, `ContextMenu`.
- Profiles without `buttons` keep working: the Quest builds the MEDIA layout from `actions`.

New profile: add `myplayer.json`, add `"myplayer"` to `index.json`, push. PotPlayer and VLC mappings are defaults from memory; tweak them if your hotkeys differ.

Marcelo Souza / Kumodot.art - 2026 // @Msouza3d - [Support Marcelo Souza](https://ko-fi.com/msouza3d)
