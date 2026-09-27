# VR Cinema App — UX/UI & Control Mapping Spec (v1)

> Target: Quest 2/3/Pro (WebXR + WebRTC bridge to PC)
> Media source: Stremio (primary), others TBD
> This doc is the single source of truth for control mapping, device behavior, and UI rules.

---

## 1. Control Architecture

### 1.1 Roles

| Controller | Role | Notes |
|---|---|---|
| **Master** (right for righties, left for lefties) | Media control, UI navigation, device interaction | Primary input device |
| **Locomotion** (opposite) | Movement in space, vertical adjust, boost | No media commands |

- "Righty" / "Lefty" selected in **Settings > Handedness**.
- The "opposite" controller is **not a mirror**. It has a reduced, dedicated button set.
- All UI is designed for the Master. Locomotion is secondary.

### 1.2 Grip-Gating (Universal Rule)

**Grip = engagement switch. No grip = no function (per that controller).**

| State | Master | Locomotion |
|---|---|---|
| Grip OFF | All buttons/stick/trigger inert | All buttons/stick/trigger inert |
| Grip ON | A/B/X/Y, Stick (UI-nav), Trigger (confirm) active | Stick (walk), Btn1 (UP), Btn2 (DOWN), Trigger (boost) active |

**Exceptions (always active, regardless of grip):**

| Input | Function | Rationale |
|---|---|---|
| JoyClick (stick click) — Locomotion | Favorite Seat Cycle | Deliberate action, cannot be accidental |
| Any HOLD (trigger hold, joyclick-hold, button hold) — Both | Extra functions (TBD) | Sustained press = intentional |
| Master pointing at Device + Trigger click | Device interaction | Aiming = intent |

### 1.3 Gaze Layer (Visual Only)

- Gaze (invisible ray from head-tracker) hitting a controller's collider **only controls visual hints/labels**.
- Gaze has **ZERO effect on functionality**. Grip is the sole functional gate.
- User can grip ON, look at screen, press buttons — works fine.

**Gaze rules:**

| Gaze | Grip | Visual |
|---|---|---|
| ON | OFF | "HOLD TO ACTIVATE" prompt above controller |
| ON | ON | Function labels rendered (Master) / movement cues (Loco) |
| OFF | OFF | Nothing rendered. Controller visually quiet. |
| OFF | ON | Nothing rendered. Still functional. |

- Labels must **not** appear in peripheral vision while user watches the screen.
- "HOLD TO ACTIVATE" text: simple, above controller, camera-facing, disappears on grip or gaze-away.

---

## 2. Master Controller — Button Map

| Input | Action | Notes |
|---|---|---|
| **Trigger (click)** | CONFIRM / SELECT | Invariant. Always confirm. Never remapped. |
| **Trigger (HOLD)** | TBD | Extra function. Anti-accidental (requires sustain). |
| **A** | Play / Pause | |
| **B** | Seek -30s | Min granularity. No fine seek. |
| **X** | Seek +30s | Min granularity. No fine seek. |
| **Y** | BACK / Exit / ESC | Closes current layer, exits fullscreen |
| **Stick (nudge)** | UI navigation (menus, lists, device) | 2D navigation of UI elements |
| **Stick (click) = JoyClick** | TBD | Extra function. |
| **Stick (click HOLD)** | TBD | Extra function. |
| **LB / RB** | TBD (candidates: Volume +/-, Subtitle size +/-) | Lower priority |

> Volume: Quest has **physical volume buttons**. In-app volume is low priority.
> Seek: No fine seek. ±30s minimum. Timeline (see §6) is a future exploration.

### 2.1 Remapping Rules (Bridge Settings)

| Tier | What | Example |
|---|---|---|
| **LOCKED** | Never changeable | Trigger=Confirm, JoyClick-Loco=Favorite Cycle, Grip-gating |
| **SWAPPABLE** | Swap within same semantic group | A↔B, X↔Y |
| **ASSIGNABLE** | Empty by default, user assigns | Stick-HOLD, Trigger-HOLD, JoyClick-HOLD |

**Action for coder:** Hide/disable the Bridge's existing freeform mapping page until this spec is signed off. Keep in code, just remove from UI. Show as "Mapping (locked — pending UX sign-off)" or omit entirely.

---

## 3. Locomotion Controller — Button Map

Reduced set. Has **2 face buttons** (either A+B or X+Y, mirrored from master). No full ABXY.

| Input | Action | Grip? |
|---|---|---|
| Stick (2D) | Walk: FWD / BACK / LEFT / RIGHT | YES |
| Btn1 (A or X) | UP (vertical +) | YES |
| Btn2 (B or Y) | DOWN (vertical −) | YES |
| Trigger (click) | BOOST / SPRINT | YES |
| Trigger (HOLD) | TBD | NO (always active) |
| JoyClick | **FAVORITE SEAT CYCLE** (teleport between saved positions) | NO (always active) |
| JoyClick (HOLD) | TBD | NO (always active) |
| Btn1 or Btn2 (HOLD) | **Recalibrate-to-Gaze** (when implemented) | NO (always active) |

> UP/DOWN: adjusts camera/avatar height. Stick is 2D only.
> Boost: sustained fast movement while trigger held (with grip).
> Favorite Seat Cycle: cycles through all saved favorite positions (teleport). Always available.

---

## 4. Device (Floating UI Panel)

### 4.1 What it is
- A floating plane/layer anchored to the **Locomotion controller** with an offset.
- Contains: media controls, info, toggles — everything that doesn't fit on the Master.

### 4.2 Positioning
- Default offset: above-behind the controller (not blocking it).
- **User-adjustable:** grip a handle area on the device to drag/reposition the offset.
- Presets (if drag is too complex): Top / Top-Left / Right / Behind.
- **Persistent:** app remembers last position. Never resets on rejoin.

### 4.3 Interaction
- **Primary:** Master controller **points at** device → laser pointer activates → Trigger click = select on device.
  - Does NOT require grip on Master (aiming = intent).
- **Secondary (TBD):** Locomotion controller buttons may also interact with device when grip is held.

### 4.4 No-Controller Mode (Hand Tracking / Gaze)
- No locomotion (no stick). Navigation = **teleport only** (Favorite Seats).
- Device appears on **palm of opposite hand** (palm up = device visible).
  - Righty: device on LEFT palm. Master hand = RIGHT.
  - Lefty: device on RIGHT palm. Master hand = LEFT.
- Interaction: pinch / tap gestures on device.
- Fallback (if hand tracking unavailable): device floats at fixed position ~0.6m in front of user.

---

## 5. Navigation / Positioning in Cinema

### 5.1 Favorite Seats (existing, keep)
- User sits in a chair (e.g., "Row 3, Seat B" → "3B").
- App records position. User adds to **Favorites** in Settings.
- **JoyClick on Locomotion** cycles through all favorites (teleport).
- Works with or without controllers (gaze + pinch for no-controller mode).

### 5.2 Recalibrate-to-Gaze (new, replaces old RECLINE)
- **Action:** One of the Locomotion face buttons in HOLD.
- **Effect:** Screen/cinema re-aligns perpendicular to user's current head orientation (line of sight).
- **Feedback:** The chair the user is in **reclines slightly** (5-10°) as visual confirmation.
- **Per-seat:** Each chair remembers its own calibration. Teleport to another chair → uses that chair's calibration (or default).
- **Not** an angle slider. It's a **snap**: "where I'm looking now = center."

### 5.3 Old RECLINE (interactive button on chair)
- **DEPRIORITIZED / BROKEN.** Multiple bugs. Do not build on this.
- Superseded by Recalibrate-to-Gaze.

---

## 6. Seek / Timeline (Future / Experimental)

- **Fine seek: DESCARTED.** Not in scope.
- Current: ±30s buttons (B/X on Master).
- **Future (P2+):** Generate a visual timeline bar representing media duration.
  - Click/drag on bar → seek to position.
  - **Blocker:** Requires bridge to set playback position in Stremio via WebRTC. Feasibility unconfirmed.
  - **Do not build until confirmed working.**

### 6.1 Media Info Display
- Bridge likely already has title/duration/position via WebRTC bidirectional channel.
- **Priority: LOW.** After core UX is stable.

---

## 7. PC Mode (Emergency Only)

- **NOT a user-facing mode.** It is a debug/emergency tool.
- **Use case:** Two apps overlap (e.g., Stremio fullscreen + POVPlayer) → need to kill one.
- **Rule:** When a media app is activated, the bridge **must kill** any other running media app. Prevent overlap proactively.
- User should **NEVER see the PC desktop**. Experience stays in the cinema.
- PC Mode = last resort. Not in main flow.

### 7.1 Stremio + ESC behavior (tested)
- `ESC` → exits fullscreen. Stremio remains maximized.
- `F` / `F11` → toggle fullscreen (alternative).
- To fully close: bridge must send kill/close command.

---

## 8. Stremio Keyboard Shortcuts (Reference for Mapping)


GLOBAL / APP Ctrl+Shift+F5 Reload App Ctrl+, Open Settings F1 / F2 / F3 / F4 Switch Tabs Ctrl+Tab Cycle Tabs Forward Ctrl+Shift+Tab Cycle Tabs Backward Backspace / Esc Exit / Go Back F / F11 Toggle Fullscreen T Show Controls

PLAYBACK Space Play / Pause Shift+N Play Next ↑ Volume Up ↓ Volume Down Shift+← Seek Prev (prev chapter/segment) Shift+→ Seek Next

SUBTITLES = Increase Subtitle Size

              Decrease Subtitle Size

H Increase Subtitle Delay G Decrease Subtitle Delay

INTERFACE O Toggle Sidebar


> Note: `Shift+←` / `Shift+→` are chapter-level seeks in Stremio (likely ~10s). For our ±30s requirement, may need multiple triggers or a custom seek command via bridge. **Verify actual seek granularity.**

---

## 9. Priority / Scope

### P0 — Must have for v1
- [ ] Grip-gating on both controllers
- [ ] Gaze-based "HOLD TO ACTIVATE" prompt
- [ ] Gaze-based labels (Master) — appear only when looking at controller
- [ ] Master button map (A/B/X/Y/Trigger/Stick) → media actions
- [ ] Locomotion: Grip + Stick = walk, A/B = up/down, Trigger = boost
- [ ] JoyClick (Loco) = Favorite Seat Cycle (always active)
- [ ] Favorite Seat system (existing, verify works)
- [ ] PC Mode kill-cross-app (bridge)
- [ ] Hide Bridge freeform mapping page
- [ ] Handedness setting (Righty/Lefty) → swaps which controller is Master vs Loco

### P1 — Should have
- [ ] Device (floating panel) on Locomotion controller with offset
- [ ] Device offset adjustment (drag or presets) + persistence
- [ ] Device interaction via Master laser pointer (no grip needed)
- [ ] Recalibrate-to-Gaze (button HOLD on Loco)
- [ ] Chair recline feedback (visual, 5-10°)
- [ ] Stremio seek verification (±30s actual behavior)

### P2 — Future / Experimental
- [ ] Timeline / seek bar (requires bridge position-set support)
- [ ] Media info on device
- [ ] Hand-tracking fallback (device on palm)
- [ ] User-assignable buttons (re-enable mapping with tiers)
- [ ] Subtitle controls (H/G/=/-)

### OUT OF SCOPE
- Fine seek
- Old RECLINE interactive chair system (broken)
- PC desktop visibility
- Stick-based look (head-tracker handles this)

---

## 10. Bridge / Architecture Notes

- Bridge likely already maps shortcuts **per-app**. **Verify before building.**
- WebRTC channel is bidirectional (app ↔ PC). Likely carries media metadata.
- Kill-cross-app: when app A activates, bridge kills app B. Must handle gracefully (no zombie windows).
- Stremio runs maximized on PC. Our VR app is the "window" the user sees. Bridge translates our VR inputs → keyboard/mouse events on PC.

---

## 11. Open Questions / TBD

| # | Question | Owner |
|---|---|---|
| 1 | Trigger-HOLD on Master: what function? | UX |
| 2 | JoyClick-HOLD on both: what function? | UX |
| 3 | LB/RB on Master: Volume? Subtitles? Or leave unassigned? | UX |
| 4 | Locomotion Btn HOLD (for Recalibrate): which of the 2? | UX |
| 5 | Does Stremio `Shift+←/→` = 10s or chapter? Need to test. | QA |
| 6 | Bridge: does it already kill other apps on activation? | Dev |
| 7 | No-controller mode: pinch = confirm? Tap = select? | UX |
| 8 | Device: does it need a "close/minimize" action? | UX |

---

## 12. Glossary

| Term | Definition |
|---|---|
| Master | The primary controller (right for righties). Media + UI. |
| Locomotion | The opposite controller. Movement + device holder. |
| Grip-gating | Rule: buttons only function when grip is held. |
| Gaze layer | Visual-only system. Labels/hints appear when head-tracker ray hits controller. |
| Device | Floating UI panel anchored to Locomotion controller. |
| Favorite Seat | Saved chair position in the cinema. Teleport target. |
| Recalibrate-to-Gaze | Snap screen alignment to current head orientation. Per-seat. |
| Boost | Fast locomotion (trigger held, grip engaged on Loco). |
| JoyClick | Clicking the analog stick. |
| Bridge | PC-side process that receives WebRTC commands and simulates keyboard/mouse for local apps. |

---

*End of spec. Next step: sign-off on P0 items, then coding.*




