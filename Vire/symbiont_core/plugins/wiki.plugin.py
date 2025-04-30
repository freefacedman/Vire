import urllib.parse
import urllib.request
import json

def wiki_cmd(args):
    if not args:
        print("Usage: wiki [topic]")
        return

    topic = " ".join(args)
    encoded = urllib.parse.quote(topic)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"

    try:
        with urllib.request.urlopen(url) as resp:
            if resp.status != 200:
                print(f"⚠️  Could not fetch page summary (HTTP {resp.status})")
                return
            data = json.load(resp)
    except Exception as e:
        print(f"⚠️  Error fetching summary: {e}")
        return

    title   = data.get("title", topic)
    extract = data.get("extract")

    if not extract:
        print(f"⚠️  No summary available for '{topic}'.")
        return

    print(f"\n🌐 Wikipedia summary for '{title}':\n")
    for line in extract.split("\n"):
        print(f"  {line}")
    print()

def register(register_command):
    register_command("wiki", wiki_cmd, aliases=["w","define"])
