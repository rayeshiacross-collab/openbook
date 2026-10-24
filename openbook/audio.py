"""Audiobook generation: free TTS engines with automatic failover."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from .book import Book
from .build import assemble
from .config import say

AUDIO_DIR_NAME = "audio"
ENGINES = ("espeak", "pyttsx3")


def _which_espeak():
    for name in ("espeak-ng", "espeak"):
        p = shutil.which(name)
        if p:
            return p
    return None


def _has_pyttsx3():
    try:
        import pyttsx3  # noqa: F401
        return True
    except ImportError:
        return False


def available_engines():
    found = []
    if _which_espeak():
        found.append("espeak")
    if _has_pyttsx3():
        found.append("pyttsx3")
    return found


def _clean_for_tts(text: str) -> str:
    t = text
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", " ", t, flags=re.S)
    t = re.sub(r"\$.*?\$", " ", t)
    t = re.sub(r"^#{1,6}\s+", "\n\n", t, flags=re.M)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"!\[.*?\]\([^)]+\)", " ", t)
    t = t.replace("**", "").replace("*", "").replace("`", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = t.replace("[VERIFY]", "")
    return t.strip()


def _split_chapters(text: str):
    chapters = re.split(r"(?m)^# ", text)
    out = []
    for ch in chapters:
        ch = ch.strip()
        if not ch:
            continue
        lines = ch.splitlines()
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        if body:
            out.append((title, body))
    return out


def _tts_espeak(text: str, out_path: Path, voice: str) -> bool:
    exe = _which_espeak()
    if not exe:
        return False
    wav = out_path.with_suffix(".wav")
    cmd = [exe, "-w", str(wav), "-s", "150", "-p", "45", "-a", "130"]
    if voice and voice != "default":
        cmd += ["-v", voice]
    cmd.append(text)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            return False
    except Exception:
        return False
    if out_path.suffix == ".wav":
        return True
    if shutil.which("ffmpeg"):
        r = subprocess.run(
            ["ffmpeg", "-y", "-i", str(wav), "-codec:a", "libmp3lame", "-q:a", "4", str(out_path)],
            capture_output=True, text=True,
        )
        wav.unlink(missing_ok=True)
        return r.returncode == 0
    return True


def _tts_pyttsx3(text: str, out_path: Path, voice: str) -> bool:
    try:
        import pyttsx3
    except ImportError:
        return False
    try:
        engine = pyttsx3.init()
        if voice and voice != "default":
            for v in engine.getProperty("voices"):
                if voice.lower() in v.id.lower() or voice.lower() in v.name.lower():
                    engine.setProperty("voice", v.id)
                    break
        engine.setProperty("rate", 150)
        engine.save_to_file(text, str(out_path))
        engine.runAndWait()
        engine.stop()
        return out_path.exists() and out_path.stat().st_size > 0
    except Exception:
        return False


ENGINE_FNS = {"espeak": _tts_espeak, "pyttsx3": _tts_pyttsx3}


def _run_with_failover(text, out_path, voice, preferred):
    order = []
    if preferred and preferred in ENGINE_FNS:
        order.append(preferred)
    for e in ENGINES:
        if e not in order:
            order.append(e)
    for eng in order:
        say(f"    trying {eng}...")
        if ENGINE_FNS[eng](text, out_path, voice):
            return eng
        say(f"    {eng} unavailable or failed; switching")
    return None


def generate_audiobook(book: Book, voice="default", fmt="mp3", preferred_engine=None):
    text, _, _ = assemble(book, include_unfinished=False)
    if not text.strip():
        raise SystemExit("Nothing to build yet: no finished sections.")
    avail = available_engines()
    if not avail:
        raise SystemExit(
            "No free TTS engine found. Install espeak-ng or: pip install pyttsx3 --user"
        )
    say(f"Available engines: {', '.join(avail)}")
    out_dir = book.out_dir / AUDIO_DIR_NAME
    out_dir.mkdir(parents=True, exist_ok=True)
    chapters = _split_chapters(text)
    say(f"Generating audiobook: {len(chapters)} chapters -> {out_dir}")
    used, files = {}, []
    for i, (title, body) in enumerate(chapters, 1):
        clean = _clean_for_tts(body)
        if not clean:
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] or f"chapter-{i}"
        out_path = out_dir / f"{i:02d}-{slug}.{fmt}"
        say(f"  chapter {i}: {title[:50]}")
        eng = _run_with_failover(clean, out_path, voice, preferred_engine)
        if eng:
            used[eng] = used.get(eng, 0) + 1
            files.append(out_path)
            say(f"    -> {out_path.name}  ({eng})")
        else:
            say(f"    FAILED: {out_path.name}")
    for eng, n in used.items():
        say(f"  {eng}: {n} chapter(s)")
    return files
