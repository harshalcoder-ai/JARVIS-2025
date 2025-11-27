# backend/open_command.py
import os
import platform
import subprocess
import webbrowser
import threading
import json
import shutil
from urllib.parse import quote_plus

# optional: pywhatkit for playonyt; fallback to opening a search results page
try:
    import pywhatkit as kit
except Exception:
    kit = None

# persistent local mapping for custom commands
_COMMANDS_FILE = os.path.join(os.path.dirname(__file__), "commands.json")

DEFAULT_MAPPINGS = {
    "youtube": "https://www.youtube.com",
    "whatsapp": "https://web.whatsapp.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
}


def _load_commands():
    if not os.path.exists(_COMMANDS_FILE):
        return {}
    try:
        with open(_COMMANDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("[open_command] failed loading commands.json:", e)
        return {}


def _save_commands(d):
    try:
        with open(_COMMANDS_FILE, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
        return True
    except Exception as e:
        print("[open_command] failed saving commands.json:", e)
        return False


def open_url(url):
    """Open URL in the default browser (non-blocking)."""
    try:
        webbrowser.open_new_tab(url)
        return True
    except Exception as e:
        print("[open_url ERROR]", e)
        return False


def open_app_by_path(path):
    """Open an app/file by path in a cross-platform way."""
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return True
    except Exception as e:
        print("[open_app_by_path ERROR]", e)
        return False


def _play_youtube_worker(term):
    """Worker that tries pywhatkit.playonyt else opens search results."""
    try:
        if kit:
            kit.playonyt(term)
        else:
            webbrowser.open_new_tab("https://www.youtube.com/results?search_query=" + quote_plus(term))
    except Exception as e:
        print("[play_youtube ERROR]", e)
        webbrowser.open_new_tab("https://www.youtube.com/results?search_query=" + quote_plus(term))


def play_youtube(search_term):
    """Start playback in background thread to avoid blocking UI."""
    t = threading.Thread(target=_play_youtube_worker, args=(search_term,), daemon=True)
    t.start()
    return True


def open_whatsapp_number(phone, message=""):
    """Open WhatsApp Web for a phone number (phone must include country code: e.g. 919876543210)."""
    try:
        encoded = quote_plus(message)
        url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded}"
        webbrowser.open_new_tab(url)
        return True
    except Exception as e:
        print("[open_whatsapp_number ERROR]", e)
        return False


def add_command(name, path):
    """Add a custom command mapping (persisted to backend/commands.json)."""
    d = _load_commands()
    d[name.lower()] = path
    return _save_commands(d)


def remove_command(name):
    d = _load_commands()
    if name.lower() in d:
        d.pop(name.lower())
        return _save_commands(d)
    return False


def open_command_router(query: str, speak_fn=None):
    """
    Main router: inspects 'query' and performs an appropriate open action.
    Returns a dict with result information so calling code (JS/Eel) receives a response.
    speak_fn(query_str) is an optional function to speak messages (pass backend.command.speak).
    """
    try:
        q = (query or "").lower().strip()
        if not q:
            return {"status": False, "error": "empty query"}

        # Load persisted app mappings
        cmds = _load_commands()

        # -- YouTube: "play <song> (on youtube)" or "play <song>"
        if "play" in q:
            # try "play X on youtube" or "play X"
            import re
            m = re.search(r"play (.+?)( on youtube| on yt|$)", q)
            if m:
                term = m.group(1).strip()
                if term:
                    if speak_fn: speak_fn(f"Playing {term} on YouTube")
                    ok = play_youtube(term)
                    return {"status": ok, "action": "play_youtube", "term": term}

        # -- Direct 'youtube' open
        if "youtube" in q:
            if speak_fn: speak_fn("Opening YouTube")
            ok = open_url(DEFAULT_MAPPINGS["youtube"])
            return {"status": ok, "action": "open_youtube"}

        # -- WhatsApp: open WhatsApp Web
        if "whatsapp" in q:
            # if message contains phone number pattern, we could extract; otherwise open WhatsApp Web
            if speak_fn: speak_fn("Opening WhatsApp Web")
            ok = open_url(DEFAULT_MAPPINGS["whatsapp"])
            return {"status": ok, "action": "open_whatsapp"}

        # -- Google / Socials
        if "google" in q:
            if speak_fn: speak_fn("Opening Google")
            ok = open_url(DEFAULT_MAPPINGS["google"])
            return {"status": ok, "action": "open_google"}

        if "facebook" in q:
            if speak_fn: speak_fn("Opening Facebook")
            ok = open_url(DEFAULT_MAPPINGS["facebook"])
            return {"status": ok, "action": "open_facebook"}

        if "instagram" in q:
            if speak_fn: speak_fn("Opening Instagram")
            ok = open_url(DEFAULT_MAPPINGS["instagram"])
            return {"status": ok, "action": "open_instagram"}

        # -- Custom mapped apps/commands persisted in commands.json
        for name, path in cmds.items():
            if name in q:
                if speak_fn: speak_fn(f"Opening {name}")
                # if path is an URL -> open
                if path.startswith("http://") or path.startswith("https://"):
                    return {"status": open_url(path), "action": "open_url", "target": path}
                # else try open as path/command
                if os.path.exists(path) or shutil.which(path):
                    return {"status": open_app_by_path(path), "action": "open_app", "target": path}
                # try to run as system command
                try:
                    if platform.system() == "Windows":
                        subprocess.Popen(path, shell=True)
                    else:
                        subprocess.Popen(path, shell=True)
                    return {"status": True, "action": "open_app", "target": path}
                except Exception as e:
                    print("[open_command_router ERROR launching mapping]", e)
                    return {"status": False, "error": str(e)}

        # -- If query looks like a URL or domain, open it
        if "http" in q or "." in q:
            url = q if q.startswith("http") else "https://" + q
            if speak_fn: speak_fn(f"Opening {url}")
            return {"status": open_url(url), "action": "open_url", "url": url}

        # -- Fallback: try to open as app (name)
        try:
            if speak_fn: speak_fn(f"Opening {q}")
            if platform.system() == "Windows":
                # os.system ensures Windows can open registered app names
                os.system(f"start {q}")
            else:
                subprocess.Popen(q, shell=True)
            return {"status": True, "action": "fallback", "target": q}
        except Exception as e:
            print("[open_command_router fallback ERROR]", e)
            return {"status": False, "error": str(e)}

    except Exception as e:
        print("[open_command_router ERROR]", e)
        return {"status": False, "error": str(e)}
