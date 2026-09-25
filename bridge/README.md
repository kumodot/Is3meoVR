# Is3meo Bridge

Small Windows helper that lets the Quest start and control the PC stream on its own.

- Waits for the Quest with a **fixed PC code (8 random characters, keep it private: it gives access to your screen and mouse)** (saved in `is3meo_bridge_config.json`).
- When the Quest connects, it **starts sharing the screen by itself** (the browser auto-selects `capture_source`, "Screen 1" in Edge).
- Opening it again closes older Bridge windows, so only one runs.
- Turns the Quest **laser pointer and buttons into real mouse and keyboard input** on Windows (SendInput).
- **Opens your player, brings it to front and makes it fullscreen** when the Quest connects (`auto_open_app`, Stremio by default) or from the VR menu (**PC: open player app**, follows the selected player profile).
- Moves the mouse cursor out of the picture when you press Play or leave PC mode.
- Uses **Microsoft Edge** by default (a separate, clean profile: your daily browser is not touched). Falls back to Chrome, then Playwright Chromium.

## Start everything from the Quest (no need to sit at the PC)

Run `add_to_startup.bat` once. From then on the Bridge starts with Windows and waits. Put on the Quest anywhere in the house, open the Light Spill Lab: it links with the saved code, the Bridge opens Stremio and starts sharing. The PC only needs to be on, awake and unlocked (a locked Windows session shows the lock screen and blocks input).

## Setup

1. Python 3.10+ and Microsoft Edge (or Chrome) installed.
2. Run `install_bridge.bat` once (installs Playwright for Python).
3. Run `run_bridge.bat`. The console shows the PC code.
4. On the Quest, open Light Spill Lab **v0.10.0+**, type the code under **PC link**, press **Connect**, keep **Auto** on.
5. Optional: `add_to_startup.bat` starts the Bridge with Windows, so the Quest can always find it.

## Quest controls (laser on the right hand)

See the controller hints in VR (they change with the mode and with ALT). Short version:

| Mode (X switches) | What the right hand does |
|---|---|
| FLY | Walk and look around. A = play/pause, B = back |
| MEDIA | Player shortcuts from the profile: stick = seek / volume, A = play/pause, B = back, trigger = player UI, grip = fullscreen. ALT: next episode, mute, subtitle size / delay |
| PC | Laser = mouse, trigger = click / drag, grip = right click, sticks = scroll, A = Enter, B = Esc. ALT: left stick = arrow keys, A = Space, B = Backspace |

## Config (`is3meo_bridge_config.json`)

| Key | Default | Meaning |
|---|---|---|
| `code` | random | The PC code the Quest connects to |
| `capture_source` | `Screen 1` | Title the browser auto-picks in the share dialog (Edge: `Screen 1`, `Screen 2`...) |
| `audio_device` | `""` | Recording device that carries the PC sound (e.g. `VoiceMeeter Aux Output`). Empty = screen share audio, which Edge does not send when the screen is auto-selected |
| `bitrate` | 15000000 | Video bitrate in bits per second |
| `apps` | auto | Exe paths per player id (`stremio`, `potplayer`, `vlc`, ...) if auto-detect fails |
| `auto_open_app` | `stremio` | Player opened / brought to front when the Quest connects (`""` = off) |
| `fullscreen_keys` | `F11` / `Enter` / `KeyF` | Key sent to each player to go fullscreen after it opens (skipped if it already is) |
| `browser` | `msedge` | `msedge`, `chrome` or `chromium` |

## Notes

- The mouse maps to the **primary monitor**, which is what "Entire screen" captures.
- The browser shows a small "sharing your screen" bar; click **Hide** once.
- Audio is sent in stereo (Opus, up to 256 kbps).

Marcelo Souza / Kumodot.art - 2026 // @Msouza3d

[Support Marcelo Souza](https://ko-fi.com/msouza3d)
