#!/usr/bin/env python3
"""
Generiert die fehlenden Wendungen-Audiodateien fuer "Italienisch Lebendig" per Azure Speech.
Einmalig auf DEINEM Computer ausfuehren (nicht im Sandbox von Claude, da dort kein
Zugriff auf externe APIs wie Azure moeglich ist).

Vorbereitung:
  1. Terminal oeffnen, in diesen Ordner wechseln:
     cd "/Users/flamrolas/Desktop/bisaya github/italienisch-lernen"
  2. Deinen Azure Speech Key als Umgebungsvariable setzen (nicht ins Skript schreiben!):
     export AZURE_SPEECH_KEY="dein-azure-key"
     export AZURE_SPEECH_REGION="eastus"   # nur noetig falls du eine andere Region nutzt
  3. Skript starten:
     python3 generate_audio_it.py

Ergebnis: ein Ordner "audio/" mit ca. 472 neuen MP3-Dateien + eine Datei
"wendungen_audio_map.json" (Text -> Dateiname). Beides bitte danach hier liegen
lassen - Claude liest die Ergebnisse direkt aus diesem Ordner und baut sie
in die App ein.
"""

import json, hashlib, os, sys, time

AZURE_KEY = os.environ.get("AZURE_SPEECH_KEY")
AZURE_REGION = os.environ.get("AZURE_SPEECH_REGION", "eastus")
VOICE = "it-IT-ElsaNeural"
TTS_URL = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"

AUDIO_DIR = "audio"
MANIFEST_FILE = "wendungen_audio_map.json"
TEXTS_FILE = "wendungen_texts_it.json"

try:
    import requests
except ImportError:
    print("Installiere benoetigtes Python-Paket 'requests' ...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

from concurrent.futures import ThreadPoolExecutor, as_completed


def filename_for(text):
    h = hashlib.md5(text.encode("utf-8")).hexdigest()[:16]
    return f"{h}.mp3"


def ssml_for(text, voice):
    esc = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
               .replace('"', "&quot;").replace("'", "&apos;"))
    return f'''<speak version="1.0" xml:lang="it-IT">
<voice name="{voice}">{esc}</voice>
</speak>'''


def synth_one(text):
    fname = filename_for(text)
    path = os.path.join(AUDIO_DIR, fname)
    if os.path.exists(path) and os.path.getsize(path) > 500:
        return (text, fname, "skip")
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-64kbitrate-mono-mp3",
        "User-Agent": "italienisch-lebendig-app",
    }
    body = ssml_for(text, VOICE).encode("utf-8")
    last_err = "unbekannt"
    for attempt in range(4):
        try:
            r = requests.post(TTS_URL, headers=headers, data=body, timeout=20)
            if r.status_code == 200 and len(r.content) > 200:
                with open(path, "wb") as f:
                    f.write(r.content)
                return (text, fname, "ok")
            elif r.status_code == 429:
                time.sleep(2 + attempt * 2)
                continue
            else:
                return (text, fname, f"error {r.status_code}: {r.text[:200]}")
        except Exception as e:
            last_err = str(e)
            time.sleep(1 + attempt)
    return (text, fname, f"error: {last_err}")


def main():
    if not AZURE_KEY:
        print("FEHLER: Umgebungsvariable AZURE_SPEECH_KEY ist nicht gesetzt.")
        print('Setze sie zuerst mit: export AZURE_SPEECH_KEY="dein-key"')
        sys.exit(1)
    if not os.path.exists(TEXTS_FILE):
        print(f"FEHLER: {TEXTS_FILE} nicht gefunden. Muss im selben Ordner liegen wie dieses Skript.")
        sys.exit(1)

    os.makedirs(AUDIO_DIR, exist_ok=True)
    texts = json.load(open(TEXTS_FILE, encoding="utf-8"))

    manifest = {}
    if os.path.exists(MANIFEST_FILE):
        manifest = json.load(open(MANIFEST_FILE, encoding="utf-8"))

    print(f"Starte Generierung fuer {len(texts)} Wendungen (Stimme: {VOICE}) ... "
          f"das dauert je nach Verbindung ca. 3-8 Minuten.")

    ok, skip, err = 0, 0, 0
    errors = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = {ex.submit(synth_one, t): t for t in texts}
        for i, fut in enumerate(as_completed(futures)):
            text, fname, status = fut.result()
            manifest[text] = fname
            if status == "ok":
                ok += 1
            elif status == "skip":
                skip += 1
            else:
                err += 1
                errors.append((text, status))
            if (i + 1) % 50 == 0 or (i + 1) == len(texts):
                json.dump(manifest, open(MANIFEST_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                print(f"Fortschritt: {i+1}/{len(texts)}  ok={ok} uebersprungen={skip} fehler={err}", flush=True)

    json.dump(manifest, open(MANIFEST_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nFERTIG. ok={ok} uebersprungen={skip} fehler={err} gesamt={len(texts)}")
    print(f"Der Ordner '{AUDIO_DIR}' und die Datei '{MANIFEST_FILE}' liegen jetzt in diesem Ordner.")
    print("Sag Claude einfach 'fertig' - der Rest (Einbau + Deploy) wird automatisch erledigt.")
    if errors:
        print("\nErste Fehler (bei Bedarf Skript einfach nochmal starten, bereits fertige Dateien werden uebersprungen):")
        for t, s in errors[:10]:
            print(" -", t[:40], "=>", s)


if __name__ == "__main__":
    main()
