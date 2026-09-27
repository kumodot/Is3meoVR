# SilVRscreen (working name) - UX & Control Spec v03

> Target: Quest 2 / 3 / Pro (WebXR) + Is3meo Bridge on the PC.
> v03 = v02 (UX chat) + build-chat review. Single source of truth for controls, screens and UI rules.
> Each controller has: thumbstick (4 directions + click), 2 face buttons, trigger, grip. Meta / Menu buttons are reserved by the system.

---

## 1. Global rules

### 1.1 Roles (Settings > Handedness)
| Controller | Role |
|---|---|
| **Master** (right for righties) | Media, navigation, pointing, confirm |
| **Locomotion** (other hand) | Moving, height, seats, holds the **Device** |

No more FLY / MEDIA / PC modes. Each hand always does the same job. PC control is a rare, explicit state (section 6).

### 1.2 Grip-gating
- Grip held = that controller's buttons work. Grip released = inert (resting hands never trigger anything).
- Always active without grip: Loco stick click (favorite seat), any HOLD action, Master pointing at a UI target + trigger.

### 1.3 Gaze = visuals only
| Gaze on controller | Grip | Shows |
|---|---|---|
| yes | no | "HOLD TO ACTIVATE" above it |
| yes | yes | button labels |
| no | any | nothing (quiet while watching) |

### 1.4 Focus and Back (the navigation rule)
There is always ONE focused layer. Master stick + trigger + B act on it:

```
PC app (Stremio / player on the big screen)   <- bottom layer
  Library panel (in front of the screen)
    Series -> episode list
  Device page (on the Loco hand)               <- top layer
```

- **Stick** = move the selection in the focused layer (in the PC app it sends arrow keys).
- **Trigger** = confirm (Enter in the PC app).
- **B** = back: closes the top layer / goes up one level. On the bottom layer it sends Esc to the PC app.
- The same three inputs work everywhere, so nothing needs to be memorized per screen.
- Our panels also accept the laser: point + trigger, same result.

---

## 2. Master controller (grip held)

| Input | Action | Label |
|---|---|---|
| Stick left / right | Arrow left / right: seek in the player, move in menus (auto-repeat while held; ~1 s held = about 30 s of seek in Stremio) | Seek / Move |
| Stick up / down | Arrow up / down: volume in the player, move in menus | Vol / Move |
| Trigger (click) | Confirm (Enter in the app). LOCKED | Select |
| Trigger (hold) | Reserved (assignable) | - |
| A | Play / Pause | Play/Pause |
| A (hold) | Show / hide the player's controls (Stremio: T) | Controls |
| B | Back (section 1.4) | Back |
| B (hold) | **Home = Library** (from anywhere) | Library |
| Stick click | Toggle the Device (show / hide, see 4) | Device |
| Stick click (hold) | Reserved (assignable) | - |

Replaces v02 "LB/RB" (they don't exist on Quest): volume and subtitles live in the Device "Now Playing" page; Up/Down already do volume in the player.

## 3. Locomotion controller

| Input | Action | Grip? |
|---|---|---|
| Stick | Walk forward / back / strafe | yes |
| Btn1 (A or X) | Up | yes |
| Btn2 (B or Y) | Down | yes |
| Trigger (held) | Boost while walking | yes |
| Stick click | **Favorite seat cycle** (teleport). LOCKED | no |
| Btn1 (hold 0.8 s) | **Recalibrate-to-gaze** (screen centered where you look, per seat) | no |
| Btn2 (hold 0.8 s) | Back to the seat (undo walking) | no |
| Stick click (hold) | Reserved | no |

## 4. The Device (panel on the Loco hand, replaces the old VR menu)

- Anchored to the Loco controller with an offset, draggable by a handle, remembered.
- Opens with Master stick click, or by turning the Loco wrist toward your face (watch gesture, 0.4 s). Closes with B, stick click, or looking away (unless pinned).
- Master laser appears only when pointing at it. Point + trigger = press.

Pages (icon tabs on top):
| Page | Contents |
|---|---|
| Now Playing | Title, play/pause, seek -30/+30, next episode, volume +/-, subtitles size/delay, fullscreen |
| Library | Opens the big library panel in front of the screen |
| Apps | Configured PC apps (Stremio, PotPlayer...) -> open one (the bridge closes the other media app first) |
| Room | Screen size, curvature, light spill + intensity, ambient, screen filter, seat row, favorites |
| Settings | Handedness, turn style, labels (auto/always/off), PC link (code, connect), VR resolution, About |
| PC | **PC control** (section 6) |
| Exit | Leave VR (hold to confirm) |

## 5. Library panel (in front of the screen)
- Open: B hold (Home), or Device > Library, or automatically when the Quest connects (Bridge setting).
- Stick moves a highlight over the posters (and the laser can point). Trigger opens. B goes back (episodes -> grid -> closes).
- Stick left/right at the grid edge = next / previous page. Stick up at the top row = category tabs.
- Playing a title closes the panel, the bridge opens the player fullscreen and closes other media apps.

## 6. PC control (rare: maintenance / emergency)
- Enter: Device > PC. The cinema screen gets a **red border** and a small "PC CONTROL" tag while active.
- Master: laser = mouse, trigger = left click / drag, A = right click, stick up/down = scroll, B (hold) = leave PC control. B tap = Esc.
- Auto-exit after 60 s without input (red border fades out). Cursor parks at the edge on exit.
- The user never sees the PC desktop in normal use.

## 7. Seats and alignment
- Favorite seats: mark in Device > Room; Loco stick click cycles them.
- Recalibrate-to-gaze (Loco Btn1 hold) replaces Recline: snaps the screen perpendicular to where you look (works lying down), saved per seat. Visual confirmation: the seat tilts 5-10 deg.
- Old Recline slider: removed.

## 8. Exit VR
- Device > Exit (hold to confirm) = main way.
- EXIT door: kept as decoration; laser + trigger still works when the Master points at it (low priority).

## 9. Bridge (PC side)
- Opening a media app closes the other running media app first (no overlap).
- Button Mapping tab moves to **Advanced**: shows the Master layout above as a help screen, allows changing assignable slots per app, with **Reset to default**.
- Stremio seek: arrows = about 10 s per press in the player; ±30 s buttons in Now Playing send 3 presses.

## 10. Stremio shortcuts (reference)
| Area | Keys |
|---|---|
| App | Ctrl+Shift+F5 reload, Ctrl+, settings, F1-F4 tabs, Ctrl+Tab / Ctrl+Shift+Tab cycle tabs, Backspace / Esc back, F / F11 fullscreen, T show controls, O sidebar |
| Playback | Space play/pause, Shift+N next, Up / Down volume, Left / Right seek, Shift+Left / Shift+Right seek (other step) |
| Subtitles | = bigger, - smaller, H delay +, G delay - |

## 11. Priorities

**P0**
- Remove FLY / MEDIA / PC modes; Master / Loco roles + handedness
- Grip-gating + "HOLD TO ACTIVATE" + gaze labels
- Focus / Back rule (1.4) across PC app, Library, Device
- Master and Loco maps (sections 2 and 3)
- Library: stick highlight navigation + B hold = Home
- Bridge: close other media app on open

**P1**
- Device panel with pages (replaces the VR menu), watch gesture, drag + remember offset
- PC control state with red border (section 6)
- Recalibrate-to-gaze per seat (+ seat tilt feedback)
- Bridge Mapping tab -> Advanced (help + reset)

**P2**
- Timeline / scrub bar and media info (needs position from the player)
- Virtual keyboard (Stremio search)
- Hand tracking (Device on the palm, pinch)
- Assignable holds (trigger hold, stick-click hold)
- EXIT door pointing polish

**Out of scope:** fine seek, Recline slider, stick look (head tracking does it).

## 12. Open questions
| # | Question |
|---|---|
| 1 | Watch gesture to open the Device: yes, or only Master stick click? |
| 2 | Loco Btn2 hold = "back to seat" OK? |
| 3 | Auto-exit PC control after 60 s: OK? |
| 4 | Library highlight: remember last position per category? |

*End of v03.*
