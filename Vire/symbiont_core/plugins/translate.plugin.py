# symbiont_core/plugins/translate.plugin.py

import urllib.request
import json

def translate_cmd(args):
    """
    Translate text into a target language using LibreTranslate.
    Usage: translate [text] [target_lang_code]
    Example: translate Hello world es
    """
    if len(args) < 2:
        print("Usage: translate [text] [target_lang_code]")
        return

    # join all but last arg as the text, last arg is target language code
    text = " ".join(args[:-1])
    target = args[-1]

    payload = json.dumps({
        "q": text,
        "source": "auto",
        "target": target,
        "format": "text"
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://libretranslate.de/translate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status != 200:
                print(f"⚠️  API error: HTTP {resp.status}")
                return
            data = json.load(resp)
    except Exception as e:
        print(f"⚠️  Error fetching translation: {e}")
        return

    translated = data.get("translatedText")
    if not translated:
        print("⚠️  No translation returned.")
        return

    print(f"\n🌐 Translation ({target}):\n  {translated}\n")

def register(register_command):
    register_command("translate", translate_cmd, aliases=["trans"])
