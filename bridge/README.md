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
4. On the Quest, open Light Spill Lab **v0.11.0+**, type the code under **PC link**, press **Connect**, keep **Auto** on.
5. Optional: `add_to_startup.bat` starts the Bridge with Windows, so the Quest can always find it.

## Quest controls

Every button has a label next to it in VR (mode color, white = same in every mode). **X** switches FLY / MEDIA / PC, hold the **left grip = ALT L** or the **right grip = ALT R** for more commands.

| Mode | Main layer (right hand) |
|---|---|
| FLY | Walk / turn, A = play/pause, B = back |
| MEDIA | Stick = seek / volume (arrows: also navigates Stremio menus), trigger = select (Enter), A = play/pause, B = back, left trigger = open player. ALT L: next episode, mute, subtitles. ALT R: fullscreen, player UI |
| PC | Laser = mouse, trigger = click / drag, sticks = scroll, A = Enter, B = Esc, left trigger = open player. ALT L: arrow keys, Space, Backspace, volume. ALT R: right click, F11, Tab |

## Settings tab (v0.6.0)

The Bridge window has a **Settings** tab: PC code, bitrate, audio device (picked from a list), captured screen, the app opened on connect, and the **apps the Quest can open**. For each app: name, exe (**Browse** opens a file picker, empty = auto detect), control profile and fullscreen key. **Test** opens it on the PC right away. **Save** writes `is3meo_bridge_config.json`.

On the Quest (Light Spill Lab v0.12.0+) the menu item **PC app** asks the Bridge for this list: stick left / right picks an app (its control profile comes along), A opens it. The left trigger in MEDIA / PC opens the picked app too.

## Button Mapping tab (v0.7.0, blueprint layout in v0.7.1)

Pick an app: the left controller's commands are listed on the left, the right one's on the right, with the controller blueprint in the middle. Every button has its own color: pick a command (or click a button on the drawing, on a stick click the side you want) and its box lights up in that color while a matching dot pulses on the real button, with the label next to it. Choose the layer (Normal, ALT L = left grip held, ALT R = right grip held), then for each button set the type (Key / Open app / Nothing), the label and the shortcut: click the key box and press it (Ctrl / Shift / Alt / Win work), or pick keys the browser keeps for itself (F11, media keys) from the list. X, Y, grips and stick clicks stay global.

**Save mapping** writes `bridge/profiles_user/<profile id>.json` and sends it to the Quest right away. **Reset to default** deletes it. If several apps share a profile, **Give <app> its own profile** splits it. **Share / JSON** shows the file to copy, or loads one someone sent you.

## Config (`is3meo_bridge_config.json`)

| Key | Default | Meaning |
|---|---|---|
| `code` | random | The PC code the Quest connects to |
| `capture_source` | `Screen 1` | Title the browser auto-picks in the share dialog (Edge: `Screen 1`, `Screen 2`...) |
| `audio_device` | `""` | Recording device that carries the PC sound (e.g. `VoiceMeeter Aux Output`). Empty = screen share audio, which Edge does not send when the screen is auto-selected |
| `bitrate` | 15000000 | Video bitrate in bits per second |
| `apps` | Stremio, PotPlayer, VLC | List of `{id, name, path, profile, fullscreen_key}`. Edit it in the Settings tab |
| `auto_open_app` | `stremio` | Player opened / brought to front when the Quest connects (`""` = off) |
| `browser` | `msedge` | `msedge`, `chrome` or `chromium` |

## Notes

- The mouse maps to the **primary monitor**, which is what "Entire screen" captures.
- The browser shows a small "sharing your screen" bar; click **Hide** once.
- Audio is sent in stereo (Opus, up to 256 kbps).

Marcelo Souza / Kumodot.art - 2026 // @Msouza3d

[Support Marcelo Souza](https://ko-fi.com/msouza3d)
