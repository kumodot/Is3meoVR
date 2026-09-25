# Is3meoVR

A virtual cinema for Meta Quest 3, with a custom 3D theater and screen light spill (the movie lights up the room). Stremio is the first media source; local files and LAN sources come later.

This repo also hosts the **Dev Launcher** on GitHub Pages: open it in the Quest Browser and tap any build to test it in VR.

## Builds

| Build | Version | What it is |
|---|---|---|
| Light Spill Lab | 0.9.1 | Labels flat on the controller face, lit controllers |
| Light Spill Lab | 0.9.0 | Per-button labels, FLY / MEDIA / PC colors, smaller EXIT, door with panic bar, stereo |
| Stream Sender | 0.3.0 | Audio from a recording device, stereo Opus |
| Is3meo Bridge | 0.3.0 | Auto-select "Screen 1" (fixes the share picker), VoiceMeeter audio, single instance |
| Light Spill Lab | 0.8.0 | Control modes + ALT layer, controller hints, player profiles, saved settings, favorite seats, EXIT sign |
| Is3meo Bridge | 0.2.0 | Edge by default, key combos for profiles, cursor park, auto-open the player, start from the Quest |
| Light Spill Lab | 0.7.0 | PC link with fixed code, laser pointer remote mouse, boost walk, new stick-click shortcuts |
| Stream Sender | 0.2.0 | PC waits with a fixed code; works with the Is3meo Bridge |
| Is3meo Bridge | 0.1.0 | Windows helper (Python + Playwright): auto share + remote mouse/keys, see `bridge/` |
| Light Spill Lab | 0.6.0 | Stand-up fix, smooth turn, hand menu, controller models, 4x3 default, modular seat kit |
| Light Spill Lab | 0.5.0 | PC stream receiver, screen size, auto aspect, custom seat GLB |
| Stream Sender | 0.1.0 | PC page that streams a tab/window/screen to the cinema (WebRTC) |
| Light Spill Lab | 0.4.0 | Curved screen with live curvature control, FPS counter |
| Light Spill Lab | 0.3.0 | In-VR menu, VR locomotion, WASD + FOV zoom, room collision, reset view, seat specular |
| Light Spill Lab | 0.2.0 | Rounded seats, lit ceiling clouds, hide UI with H |
| Light Spill Lab | 0.1.0 | First screen light spill prototype (Three.js / WebXR) |

## Run locally

Double-click `run_launcher.bat` (needs Python). It serves the repo on port 8080 and opens the launcher.

Quest over USB (developer mode + adb):

```
adb reverse tcp:8080 tcp:8080
```

Then open `http://localhost:8080/` in the Quest Browser.

## Adding a new build

1. Save it with the version in the file name, e.g. `light_spill_lab/light_spill_lab_v0.3.0.html`.
2. Add an entry at the top of `BUILDS` in `index.html`.
3. Push. GitHub Pages updates in about a minute.

## Credits

Marcelo Souza / Kumodot.art - 2026 // @Msouza3d

[Support Marcelo Souza](https://ko-fi.com/msouza3d)
