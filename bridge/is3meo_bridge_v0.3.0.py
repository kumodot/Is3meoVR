"""
Is3meo Bridge v0.3.0
Marcelo Souza / Kumodot.art - 2026 // @Msouza3d
Support Marcelo Souza: https://ko-fi.com/msouza3d

Runs on the Windows PC. It opens the Is3meo Stream Sender in a Chrome window driven by Playwright,
waits for the Quest with a fixed code, starts sharing the screen by itself when the Quest connects,
and turns the Quest's laser pointer / buttons into real mouse and keyboard input on Windows.

Setup: run install_bridge.bat once, then run_bridge.bat (or add_to_startup.bat to start with Windows).
"""
import asyncio
import ctypes
import glob
import json
import os
import random
import subprocess
import sys
import time
import webbrowser
from ctypes import wintypes
from pathlib import Path

VERSION = '0.3.0'
CONFIG_VERSION = 3
HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / 'is3meo_bridge_config.json'
DEFAULTS = {
    'code': None,                      # 4 digit PC code, created on first run
    'sender_url': 'https://kumodot.github.io/Is3meoVR/stream_sender/stream_sender_v0.3.0.html',
    'capture_source': 'Screen 1',       # title the browser auto-selects in the share picker (Edge: 'Screen 1')
    'audio_device': '',                 # recording device that carries the PC sound, e.g. 'VoiceMeeter Aux Output' ('' = share audio)
    'bitrate': 15000000,
    'stremio_path': '',                 # empty = auto detect, falls back to web.stremio.com
    'browser': 'msedge',                # msedge, chrome or chromium (Playwright's own). Separate profile, your daily browser is untouched
    'apps': {                           # players the Quest can open ("PC: open player app"), empty = auto detect
        'stremio': '',
        'potplayer': '',
        'vlc': '',
    },
    'auto_open_app': 'stremio',         # opened when the Quest connects and it is not running ('' = off)
    'config_version': CONFIG_VERSION,
}


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
def load_config():
    cfg = dict(DEFAULTS)
    if CONFIG_PATH.exists():
        try:
            cfg.update(json.loads(CONFIG_PATH.read_text(encoding='utf-8')))
        except Exception as e:
            print('Config unreadable, using defaults:', e)
    if cfg.get('config_version', 1) < 2:
        # v0.1.0 configs: move to Edge and add the new keys, keep the code
        cfg['browser'] = 'msedge'
        cfg.pop('chrome_channel', None)
        cfg['config_version'] = CONFIG_VERSION
    if cfg.get('config_version', 1) < 3:
        # v0.2.0 configs: Edge names the monitor "Screen 1", newer sender page
        if cfg.get('capture_source') in (None, '', 'Entire screen'):
            cfg['capture_source'] = 'Screen 1'
        cfg['sender_url'] = DEFAULTS['sender_url']
        cfg['config_version'] = CONFIG_VERSION
    for k, v in DEFAULTS.items():
        cfg.setdefault(k, v)
    if not cfg.get('code') or not str(cfg['code']).isdigit() or len(str(cfg['code'])) != 4:
        cfg['code'] = str(random.randint(1000, 9999))
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding='utf-8')
    return cfg


# ---------------------------------------------------------------------------
# Windows input injection (SendInput)
# ---------------------------------------------------------------------------
user32 = ctypes.WinDLL('user32', use_last_error=True)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # per-monitor DPI aware
except Exception:
    pass

INPUT_MOUSE, INPUT_KEYBOARD = 0, 1
MOUSEEVENTF_MOVE, MOUSEEVENTF_ABSOLUTE = 0x0001, 0x8000
MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP = 0x0002, 0x0004
MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP = 0x0008, 0x0010
MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP = 0x0020, 0x0040
MOUSEEVENTF_WHEEL = 0x0800
KEYEVENTF_EXTENDEDKEY, KEYEVENTF_KEYUP = 0x0001, 0x0002
ULONG_PTR = ctypes.c_size_t


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [('dx', wintypes.LONG), ('dy', wintypes.LONG), ('mouseData', wintypes.DWORD),
                ('dwFlags', wintypes.DWORD), ('time', wintypes.DWORD), ('dwExtraInfo', ULONG_PTR)]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [('wVk', wintypes.WORD), ('wScan', wintypes.WORD), ('dwFlags', wintypes.DWORD),
                ('time', wintypes.DWORD), ('dwExtraInfo', ULONG_PTR)]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [('uMsg', wintypes.DWORD), ('wParamL', wintypes.WORD), ('wParamH', wintypes.WORD)]


class _INPUTUNION(ctypes.Union):
    _fields_ = [('mi', MOUSEINPUT), ('ki', KEYBDINPUT), ('hi', HARDWAREINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [('type', wintypes.DWORD), ('u', _INPUTUNION)]


def _send(*items):
    arr = (INPUT * len(items))(*items)
    user32.SendInput(len(items), arr, ctypes.sizeof(INPUT))


def _mouse(flags, dx=0, dy=0, data=0):
    i = INPUT(type=INPUT_MOUSE)
    i.u.mi = MOUSEINPUT(dx, dy, data & 0xFFFFFFFF, flags, 0, 0)
    return i


# Virtual key codes for the keys the Quest can send (profiles use these names)
VK = {
    'Escape': 0x1B, 'Enter': 0x0D, 'Space': 0x20, 'Backspace': 0x08, 'Tab': 0x09, 'Delete': 0x2E, 'Insert': 0x2D,
    'ArrowLeft': 0x25, 'ArrowUp': 0x26, 'ArrowRight': 0x27, 'ArrowDown': 0x28,
    'PageUp': 0x21, 'PageDown': 0x22, 'End': 0x23, 'Home': 0x24,
    'Equal': 0xBB, 'Minus': 0xBD, 'Comma': 0xBC, 'Period': 0xBE, 'Slash': 0xBF, 'Semicolon': 0xBA,
    'BracketLeft': 0xDB, 'BracketRight': 0xDD, 'Quote': 0xDE, 'Backquote': 0xC0,
    'MediaPlayPause': 0xB3, 'MediaNextTrack': 0xB0, 'MediaPrevTrack': 0xB1, 'MediaStop': 0xB2,
    'VolumeUp': 0xAF, 'VolumeDown': 0xAE, 'VolumeMute': 0xAD,
    'Shift': 0x10, 'Control': 0x11, 'Alt': 0x12,
}
VK.update({f'Key{chr(c)}': c for c in range(ord('A'), ord('Z') + 1)})
VK.update({f'Digit{d}': 0x30 + d for d in range(10)})
VK.update({f'F{n}': 0x6F + n for n in range(1, 13)})
EXTENDED = {0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x2D, 0x2E}


def _key(vk, up=False):
    flags = (KEYEVENTF_KEYUP if up else 0) | (KEYEVENTF_EXTENDEDKEY if vk in EXTENDED else 0)
    i = INPUT(type=INPUT_KEYBOARD)
    i.u.ki = KEYBDINPUT(vk, 0, flags, 0, 0)
    return i


BUTTONS = {0: (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
           1: (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP),
           2: (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP)}


def move_to(x, y):
    # Absolute coords 0..65535 over the primary monitor (the captured "Entire screen")
    x = min(max(float(x), 0.0), 1.0)
    y = min(max(float(y), 0.0), 1.0)
    _send(_mouse(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, int(x * 65535), int(y * 65535)))


def handle_input(msg, cfg):
    """Messages from the Quest: move / down / up / click / wheel / key / cmd."""
    try:
        t = msg.get('t')
        if t == 'move':
            move_to(msg['x'], msg['y'])
        elif t in ('down', 'up'):
            d, u = BUTTONS.get(int(msg.get('b', 0)), BUTTONS[0])
            _send(_mouse(d if t == 'down' else u))
        elif t == 'click':
            d, u = BUTTONS.get(int(msg.get('b', 0)), BUTTONS[0])
            _send(_mouse(d), _mouse(u))
        elif t == 'wheel':
            _send(_mouse(MOUSEEVENTF_WHEEL, data=int(msg.get('d', 120))))
        elif t == 'key':
            vk = VK.get(msg.get('k'))
            if vk:
                mods = [VK[m] for m in (msg.get('mods') or []) if m in VK]
                seq = [_key(m) for m in mods] + [_key(vk), _key(vk, up=True)] + [_key(m, up=True) for m in reversed(mods)]
                _send(*seq)
        elif t == 'park':
            move_to(0.9995, 0.5)  # cursor out of the way (right edge) so players hide their UI
        elif t == 'cmd' and msg.get('c') in ('openStremio', 'openApp'):
            open_app(cfg, msg.get('app') or 'stremio')
    except Exception as e:
        print('Input error:', e, msg)


# ---------------------------------------------------------------------------
# Stremio launcher
# ---------------------------------------------------------------------------
def find_stremio(cfg):
    if cfg.get('stremio_path') and Path(cfg['stremio_path']).exists():
        return cfg['stremio_path']
    roots = [os.environ.get('LOCALAPPDATA', ''), os.environ.get('ProgramFiles', ''), os.environ.get('ProgramFiles(x86)', '')]
    for root in roots:
        if not root:
            continue
        for pattern in ('Programs/LNV/Stremio*/stremio*.exe', 'Programs/Stremio*/stremio*.exe', 'Stremio*/stremio*.exe'):
            hits = [h for h in glob.glob(os.path.join(root, pattern)) if 'uninstall' not in h.lower()]
            if hits:
                return hits[0]
    return None


KNOWN_APPS = {
    'potplayer': [r'C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe', r'C:\Program Files (x86)\DAUM\PotPlayer\PotPlayerMini.exe'],
    'vlc': [r'C:\Program Files\VideoLAN\VLC\vlc.exe', r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe'],
}


def find_app(cfg, app):
    path = (cfg.get('apps') or {}).get(app) or ''
    if path and Path(path).exists():
        return path
    if app == 'stremio':
        return find_stremio(cfg)
    for cand in KNOWN_APPS.get(app, []):
        if Path(cand).exists():
            return cand
    return None


def is_running(exe_path):
    try:
        name = Path(exe_path).name
        out = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {name}', '/NH'], capture_output=True, text=True, timeout=5).stdout
        return name.lower() in out.lower()
    except Exception:
        return False


def open_app(cfg, app):
    exe = find_app(cfg, app)
    if exe:
        print(f'Opening {app}:', exe)
        subprocess.Popen([exe], cwd=str(Path(exe).parent))
    elif app == 'stremio':
        print('Stremio app not found, opening web.stremio.com (set apps.stremio in the config to fix)')
        webbrowser.open('https://web.stremio.com')
    else:
        print(f'{app} not found. Set its exe path under "apps" in {CONFIG_PATH.name}')


_last_auto_open = 0.0


def auto_open(cfg):
    global _last_auto_open
    app = cfg.get('auto_open_app') or ''
    if not app or time.time() - _last_auto_open < 15:
        return
    _last_auto_open = time.time()
    exe = find_app(cfg, app)
    if exe and is_running(exe):
        return
    open_app(cfg, app)


# ---------------------------------------------------------------------------
# Sender page driven by Playwright
# ---------------------------------------------------------------------------
async def run(cfg):
    from playwright.async_api import async_playwright

    from urllib.parse import quote, urlparse
    url = f"{cfg['sender_url']}?code={cfg['code']}&bitrate={cfg['bitrate']}&audioDevice={quote(cfg.get('audio_device') or '')}&t={int(time.time())}"
    args = [
        f"--auto-select-desktop-capture-source={cfg['capture_source']}",
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding',
        '--disable-backgrounding-occluded-windows',
        '--autoplay-policy=no-user-gesture-required',
    ]
    async with async_playwright() as pw:
        browser = None
        order = [cfg.get('browser') or 'msedge'] + [b for b in ('msedge', 'chrome', 'chromium') if b != cfg.get('browser')]
        for name in order:
            try:
                channel = None if name == 'chromium' else name
                browser = await pw.chromium.launch(channel=channel, headless=False, args=args)
                print('Using browser:', name)
                break
            except Exception as e:
                print(f'{name} not available:', str(e).splitlines()[0])
        if browser is None:
            print('No browser found. Install Edge or Chrome, or run: python -m playwright install chromium')
            return
        ctx = await browser.new_context(no_viewport=True)
        if cfg.get('audio_device'):
            u = urlparse(cfg['sender_url'])
            await ctx.grant_permissions(['microphone'], origin=f'{u.scheme}://{u.netloc}')
        page = await ctx.new_page()
        share_lock = asyncio.Lock()

        async def minimize():
            try:
                cdp = await ctx.new_cdp_session(page)
                w = await cdp.send('Browser.getWindowForTarget')
                await cdp.send('Browser.setWindowBounds', {'windowId': w['windowId'], 'bounds': {'windowState': 'minimized'}})
            except Exception as e:
                print('Could not minimize the sender window:', e)

        async def do_share():
            async with share_lock:
                try:
                    await page.bring_to_front()
                    if await page.is_disabled('#btnShare'):
                        return  # already sharing
                    await page.click('#btnShare', timeout=5000)  # a real click = user gesture for getDisplayMedia
                except Exception as e:
                    print('Auto share failed:', e)

        def on_request_share():
            # The Quest connected: open the player if needed, then share the screen
            loop = asyncio.get_running_loop()
            loop.run_in_executor(None, auto_open, cfg)
            loop.create_task(do_share())

        async def on_share_started(info):
            print(f"Sharing the screen (audio tracks: {info.get('audio', 0)})")
            await minimize()

        await page.expose_function('is3meoInput', lambda m: handle_input(m, cfg))
        await page.expose_function('is3meoRequestShare', on_request_share)
        await page.expose_function('is3meoShareStarted', on_share_started)
        await page.expose_function('is3meoLog', lambda m: print('[sender]', m))
        await page.goto(url)

        print()
        print('=' * 60)
        print(f'  Is3meo Bridge v{VERSION}  -  PC code: {cfg["code"]}')
        print('  Type this code once on the Quest (Light Spill Lab v0.7.0+).')
        print('  Keep this window open. Ctrl+C to quit.')
        print('=' * 60)
        print()
        while not page.is_closed():
            await asyncio.sleep(1)
        await browser.close()


def kill_other_instances():
    """Close older Bridge windows (python + their run_bridge.bat console + their browser)."""
    keep = {os.getpid(), os.getppid()}
    ps = (
        "Get-CimInstance Win32_Process | Where-Object { "
        "($_.Name -like 'python*' -and $_.CommandLine -like '*is3meo_bridge_v*') -or "
        "($_.Name -eq 'cmd.exe' -and $_.CommandLine -like '*run_bridge.bat*') -or "
        "(($_.Name -eq 'msedge.exe' -or $_.Name -eq 'chrome.exe') -and $_.CommandLine -like '*playwright*') "
        "} | Select-Object ProcessId | ConvertTo-Json -Compress"
    )
    try:
        out = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True, timeout=30).stdout.strip()
        procs = json.loads(out) if out else []
        if isinstance(procs, dict):
            procs = [procs]
        killed = 0
        for p in procs:
            pid = int(p.get('ProcessId', 0))
            if pid and pid not in keep:
                subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'], capture_output=True)
                killed += 1
        if killed:
            print(f'Closed {killed} old Bridge process(es).')
    except Exception as e:
        print('Could not check for old Bridge instances:', e)


def main():
    print(f'Is3meo Bridge v{VERSION} - Marcelo Souza / Kumodot.art - 2026 // @Msouza3d')
    print('Support Marcelo Souza: https://ko-fi.com/msouza3d')
    if sys.platform != 'win32':
        print('The Bridge injects Windows input and only runs on Windows.')
        return
    kill_other_instances()
    cfg = load_config()
    try:
        asyncio.run(run(cfg))
    except KeyboardInterrupt:
        pass
    except ModuleNotFoundError:
        print('Playwright is missing. Run install_bridge.bat first.')


if __name__ == '__main__':
    main()
