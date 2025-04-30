import urllib.parse
import urllib.request
import json

def dictionary_cmd(args):
    """
    Look up definitions using the Free Dictionary API.
    Usage: define [word]
    """
    if not args:
        print("Usage: define [word]")
        return

    word = args[0]
    encoded = urllib.parse.quote(word)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{encoded}"

    try:
        with urllib.request.urlopen(url) as resp:
            if resp.status != 200:
                print(f"⚠️  No entry found for '{word}'.")
                return
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"⚠️  No definition found for '{word}'.")
        else:
            print(f"⚠️  HTTP error {e.code}")
        return
    except Exception as e:
        print(f"⚠️  Error fetching definition: {e}")
        return

    # data is a list of entries
    for entry in data:
        word_text = entry.get("word", word)
        print(f"\n📖 Definitions for '{word_text}':\n")
        for meaning in entry.get("meanings", []):
            part = meaning.get("partOfSpeech", "")
            print(f"➤ {part}")
            for d in meaning.get("definitions", []):
                defi = d.get("definition")
                example = d.get("example")
                print(f"   – {defi}")
                if example:
                    print(f"     e.g. “{example}”")
            print()
    print()

def register(register_command):
    register_command("define", dictionary_cmd, aliases=["dict","def"])
