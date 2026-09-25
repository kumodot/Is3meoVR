# Is3meo Bridge

Small Windows helper that lets the Quest start and control the PC stream on its own.

- Waits for the Quest with a **fixed 4 digit PC code** (saved in `is3meo_bridge_config.json`).
- When the Quest connects, it **starts sharing the screen by itself** (Chrome auto-selects "Entire screen").
- Turns the Quest **laser pointer and buttons into real mouse and keyboard input** on Windows (SendInput).
- **Open Stremio** from the VR menu (auto-detects the Stremio app, falls back to web.stremio.com).

## Setup

1. Python 3.10+ and Google Chrome installed.
2. Run `install_bridge.bat` once (installs Playwright for Python).
3. Run `run_bridge.bat`. The console shows the PC code.
4. On the Quest, open Light Spill Lab **v0.7.0+**, type the code under **PC link**, press **Connect**, keep **Auto** on.
5. Optional: `add_to_startup.bat` starts the Bridge with Windows, so the Quest can always find it.

## Quest controls (laser on the right hand)

| Action | Result on the PC |
|---|---|
| Point at the screen | Moves the mouse |
| Trigger | Left click (hold to drag) |
| Grip | Right click |
| Right stick up/down (pointing at the screen) | Scroll |
| B | Esc (back) |
| Menu: PC open Stremio / play-pause / fullscreen / back | Launch Stremio, Space, F11, Esc |

## Config (`is3meo_bridge_config.json`)

| Key | Default | Meaning |
|---|---|---|
| `code` | random | The PC code the Quest connects to |
| `capture_source` | `Entire screen` | Title Chrome auto-picks in the share dialog (try `Screen 1` with more monitors) |
| `bitrate` | 15000000 | Video bitrate in bits per second |
| `stremio_path` | auto | Full path to the Stremio exe if auto-detect fails |
| `chrome_channel` | `chrome` | Empty string to use Playwright Chromium instead |

## Notes

- The mouse maps to the **primary monitor**, which is what "Entire screen" captures.
- Chrome shows a small "sharing your screen" bar; click **Hide** once.
- Audio: with "Entire screen" Chrome sends system audio when available.

Marcelo Souza / Kumodot.art - 2026 // @Msouza3d

[Support Marcelo Souza](https://ko-fi.com/msouza3d)
