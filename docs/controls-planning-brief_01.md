# Is3meoVR / SilVRscreen - Controls planning brief

Handoff for a UX planning chat. Goal: redesign the default controls of every mode and the navigation between screens, then bring the plan back to the build chat to implement in one go. Current build: Light Spill Lab v0.15.0 (Quest 3, WebXR) + Is3meo Bridge v0.10.1 (PC).

## Hardware limits (Quest 3 Touch Plus in WebXR)
- Usable per controller: trigger (analog), grip (analog), thumbstick (x/y + click), 2 face buttons (A/B right, X/Y left). Thumb rests (touch) exist but are unreliable.
- NOT available to WebXR apps: Meta button (right) and Menu button (left), both reserved by the system.
- Tricks we can use: hold vs tap (already: Y tap = menu, Y hold 0.6 s = library), double tap, "ALT layers" (a grip held changes what the other buttons do), gaze (looking at a controller), laser pointer + trigger.
- Every button can show a label floating next to it (already built), colored by mode.

## Screens / states today
1. Cinema (watching). Three control modes, X cycles them:
   - FLY (red): move around the room, tweak the room.
   - MEDIA (green): control the PC player with keyboard shortcuts from the app's profile.
   - PC (blue): laser = mouse, keyboard keys.
2. Menu (Y tap): list of settings/actions, attached to the left controller.
3. Library (Y hold): poster grid of the PC media folders, series -> episode list.
4. EXIT door/sign in the room: aim + trigger leaves VR.

## Current mapping (v0.15.0)
Global (all modes): Y tap = menu, Y hold = library, X = next mode (ALT L + X = previous), L3 (left stick click) = next favorite seat + recenter, R3 = light spill on/off, left grip hold = ALT L, right grip hold = ALT R, right trigger on menu / EXIT / library = click.

FLY
- Base: L stick walk, left trigger = speed boost, R stick = turn (snap/smooth) + up/down, A = play/pause, B = back.
- ALT L: R stick = screen size / light intensity, A = laser mode, B = hints mode.
- ALT R: R stick = curvature / ambient light, A = next demo scene, B = favorite seat toggle.

MEDIA (per app, editable in the Bridge "Button Mapping" tab; defaults below)
- Base: R stick left/right = seek -/+, up/down = volume, L stick left/right = small seek, A = play/pause, B = back, right trigger = Select (Enter), left trigger = open the picked app.
- ALT L: A = next episode, B = mute, R stick = subtitle delay / size.
- ALT R: A = fullscreen, B = player UI, right trigger = open app.

PC
- Base: laser = mouse, right trigger = click/drag, sticks = scroll, A = Enter, B = Esc, left trigger = open app.
- ALT L: L stick = arrow keys, A = Space, B = Backspace, R stick = volume.
- ALT R: A = F11, B = Tab, right trigger = right click.

Menu open: L stick up/down = move, R stick left/right = change value, A or left trigger = confirm, laser + trigger = click a row.
Library open: laser + trigger = open/play, sticks left/right = pages, R stick up/down = category, B = back (episode list -> grid -> close).

## Known pain points (to confirm / expand)
- Too many things hidden behind ALT layers; hard to remember.
- Three modes + X cycling is confusing; not always clear which mode you are in.
- Navigation between Cinema / Menu / Library / PC is not consistent (different "back" buttons).
- MEDIA vs PC overlap (both send keys to the PC).
- Recline (lying down) and seat/recenter need an easy, safe control.

## What the planning chat should deliver
1. The list of states/screens and how you move between them (a simple flow: what opens what, what "back" does everywhere).
2. A full table per state: button -> action (base, and ALT only if really needed), plus hold/tap/double-tap where used.
3. Which buttons stay global (same everywhere) and why.
4. Label text for each button (max ~14 characters).
5. Anything to remove or move into the menu.
Plain markdown tables are perfect. Save it as `claude/controls-plan.md` in this project, then bring it back to the build chat.

## Every interaction the app has today (v0.15.0)

### VR menu (Y tap) - all items
Sliders (stick left/right changes the value): Light spill (on/off), Screen size, Curvature, Intensity (light), Specular, Smoothing, Blur, Ambient, Zones (4x3 up to 8x5).
Choices / actions: Source (demo / video file / PC stream), Demo scene, Play / Pause, Library (hold Y), Recline (0-80 deg, lying down), PC link (connect / disconnect, remembered code, auto reconnect), PC app (pick which configured PC app, A opens it; the control profile follows the app), Control mode (FLY / MEDIA / PC), Player profile (Stremio, PotPlayer, VLC, generic, custom), Seat row, Favorite seat (mark rows, L3 cycles them), Laser (auto / on / off; auto = only in PC mode, menu, library or aiming at EXIT), Button hints (auto fade / always / off), Screen filter (sharp / balanced / smooth), VR resolution, Turn (snap 30 deg / smooth), Next favorite seat, Close menu.

### Things in the room
- EXIT door + EXIT sign: aim the laser, trigger = leave VR.
- Gaze light: looking at a controller lights it up softly and shows its button labels.
- Mode title label above the left controller (mode + ALT layer + current profile).
- Toasts: short messages in front of you (mode changed, playing X, etc.).
- Library panel in front of the screen: category tabs, player picker (top right), close, poster grid (7 x 2), backdrop + synopsis of the aimed title, page arrows, rescan; series open an episode list with Back.

### Desktop (browser, not in VR)
- Mouse drag = look, WASD = walk, scroll = zoom (FOV), R = reset view, H = hide the side panel, L = light on/off, N = next demo scene, Space = play/pause.
- Side panel: the same sliders as the VR menu, Demo reel, Load video..., Play/Pause, PC code + Connect + Auto, Load GLB room..., Default room, Load seat GLB..., Load armrest GLB..., Reset seat kit, Download seat kit, Reset view, About, Enter VR button.

### PC side (Is3meo Bridge window, tabs)
- Stream: code, bitrate, frame rate, Share / Stop, status, preview.
- Settings: PC code, bitrate, audio device, captured screen, what opens when the Quest connects (nothing / media library / an app), PC speakers while linked (VoiceMeeter mute), apps list (name, exe + Browse, Test, profile, fullscreen key, type app/player, open-file args), media library (categories, folders, default player, Rescan), artwork (optional own TMDB key, fanart.tv key, language).
- Button Mapping: per app, per layer (Normal / ALT L / ALT R), label + shortcut for each MEDIA button on the controller blueprint, Save / Reset / Share JSON.

### Automatic behaviors
- Quest connects -> Bridge shares the screen, opens the chosen app or the library, mutes PC speakers (if set).
- Playing from the library -> player opens fullscreen, Quest switches to MEDIA + that player's profile.
- Cursor parks at the screen edge after play/pause and when leaving PC mode.
- Settings persist on the Quest (seat, mode, profile, laser, hints, filter, recline, etc.).
