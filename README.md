# Is3meoVR

A virtual cinema for Meta Quest 3, with a custom 3D theater and screen light spill (the movie lights up the room). Stremio is the first media source; local files and LAN sources come later.

This repo also hosts the **Dev Launcher** on GitHub Pages: open it in the Quest Browser and tap any build to test it in VR.

## Builds

| Build | Version | What it is |
|---|---|---|
| Is3meo Bridge | 0.8.1 | Opens Stream Sender 0.7.1 |
| Stream Sender | 0.7.1 | Fix: 40 Mbps shows on the Stream tab |
| Is3meo Bridge | 0.8.0 | Optional: mute the VoiceMeeter speaker outputs while the Quest is linked |
| Stream Sender | 0.7.0 | PC speakers setting |
| Is3meo Bridge | 0.7.1 | Opens Stream Sender 0.6.0 |
| Stream Sender | 0.6.0 | Button Mapping on the controller blueprint with colored markers |
| Light Spill Lab | 0.13.0 | MEDIA buttons + labels from the Bridge Button Mapping |
| Is3meo Bridge | 0.7.0 | Button Mapping tab: draw-and-map the Quest buttons per app (with Stream Sender 0.5.0) |
| Stream Sender | 0.5.0 | Button Mapping tab |
| Light Spill Lab | 0.12.0 | PC app picker: asks the Bridge for its app list, profile follows the app |
| Is3meo Bridge | 0.6.0 | Settings tab: any player exe + profile + fullscreen key, audio device list |
| Stream Sender | 0.4.0 | Stream + Settings tabs, app list for the Quest |
| Light Spill Lab | 0.11.0 | Labels on every button, ALT L + ALT R, MEDIA select, screen filter option |
| Is3meo Bridge | 0.5.0 | Maximized is not fullscreen: sends F11 when needed |
| Light Spill Lab | 0.10.0 | Laser only when needed, gaze-lit controllers, fixed label lines + swap, open player from VR, sharper screen, VR resolution |
| Is3meo Bridge | 0.4.0 | Opens the real stremio.exe (not the runtime), brings the player to front + fullscreen |
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
