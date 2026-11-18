"""Vertont alle Texte aus dem Ordner texte/ mit deiner eigenen HeyGen-Stimme.

Läuft automatisch in GitHub, sobald du einen Text in texte/ ablegst oder änderst.
Die fertigen MP3-Dateien landen im Ordner audio/.
Deine Schlüssel liegen als Secrets in dieser Werkstatt (HEYGEN_API_KEY, HEYGEN_VOICE_ID).
"""
import hashlib, json, os, re, sys, urllib.error, urllib.request
from pathlib import Path

KEY = os.environ.get("HEYGEN_API_KEY", "").strip()
VOICE = os.environ.get("HEYGEN_VOICE_ID", "").strip()
ROOT = Path(__file__).resolve().parent.parent
TEXTE, AUDIO = ROOT / "texte", ROOT / "audio"
MAX = 9000  # HeyGen nimmt bis 10.000 Zeichen pro Aufruf, wir teilen vorher
AUSSPRACHE = ROOT / "werkzeug" / "aussprache.txt"


def aussprache():
    """Liest werkzeug/aussprache.txt: pro Zeile „Wort = so gesprochen“."""
    regeln = []
    if AUSSPRACHE.exists():
        for zeile in AUSSPRACHE.read_text(encoding="utf-8").splitlines():
            if "=" in zeile and not zeile.strip().startswith("#"):
                wort, gesprochen = (t.strip() for t in zeile.split("=", 1))
                if wort and gesprochen:
                    regeln.append((re.compile(r"\b" + re.escape(wort) + r"\b", re.IGNORECASE), gesprochen))
    return regeln


def sprechtext(text, regeln):
    for muster, gesprochen in regeln:
        text = muster.sub(gesprochen, text)
    return text


def call(body):
    req = urllib.request.Request("https://api.heygen.com/v3/models/audio/tts", method="POST",
        data=json.dumps(body).encode(),
        headers={"X-Api-Key": KEY, "Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}


def stuecke(text):
    """Teilt lange Texte an Absätzen in Stücke unter MAX Zeichen."""
    teile, akt = [], ""
    for absatz in text.split("\n\n"):
        if akt and len(akt) + len(absatz) + 2 > MAX:
            teile.append(akt)
            akt = ""
        akt = (akt + "\n\n" + absatz).strip()
    if akt:
        teile.append(akt)
    return teile


def main():
    if not KEY or not VOICE:
        print("Noch keine Schlüssel in der Werkstatt. Verbinde HeyGen in der Startanleitung des Bestager-Bauplans.")
        return
    AUDIO.mkdir(exist_ok=True)
    regeln = aussprache()
    regel_text = AUSSPRACHE.read_text(encoding="utf-8") if AUSSPRACHE.exists() else ""
    fehler = 0
    for txt in sorted(TEXTE.glob("*.txt")):
        text = txt.read_text(encoding="utf-8").strip()
        if not text:
            continue
        h = hashlib.sha256((text + VOICE + regel_text).encode()).hexdigest()[:16]
        meta = AUDIO / (txt.stem + ".json")
        mp3 = AUDIO / (txt.stem + ".mp3")
        if mp3.exists() and meta.exists() and json.loads(meta.read_text()).get("hash") == h:
            print("unverändert:", txt.name)
            continue
        daten, dauer = b"", 0.0
        for teil in stuecke(sprechtext(text, regeln)):
            st, d = call({"voice_id": VOICE, "text": teil, "model": "heygen-voice-1", "language": "de",
                          "output_format": {"encoding": "mp3", "sample_rate_hertz": 44100, "bitrate_bps": 192000}})
            data = d.get("data", d) if isinstance(d, dict) else {}
            if st != 200 or not data.get("audio_url"):
                print("Fehler bei", txt.name, st, d.get("error", ""))
                fehler += 1
                break
            with urllib.request.urlopen(data["audio_url"], timeout=300) as r:
                daten += r.read()
            dauer += float(data.get("duration") or 0)
        else:
            mp3.write_bytes(daten)
            meta.write_text(json.dumps({"hash": h, "sekunden": round(dauer, 1), "zeichen": len(text)}))
            print("fertig:", mp3.name, round(dauer, 1), "Sekunden")
    if fehler:
        sys.exit(1)


main()
