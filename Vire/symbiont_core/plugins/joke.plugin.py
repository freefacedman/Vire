# symbiont_core/plugins/joke.plugin.py

import urllib.request
import json

def joke_cmd(args):
    """
    Fetch a random joke from the Official Joke API.
    Usage: joke
    """
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        with urllib.request.urlopen(url) as resp:
            if resp.status != 200:
                print(f"⚠️  Could not fetch joke (HTTP {resp.status})")
                return
            data = json.load(resp)
    except Exception as e:
        print(f"⚠️  Error fetching joke: {e}")
        return

    setup = data.get("setup")
    punch = data.get("punchline")
    if setup and punch:
        print(f"\n😂 {setup}")
        print(f"👉 {punch}\n")
    else:
        print("⚠️  Joke data malformed.")

def register(register_command):
    register_command("joke", joke_cmd, aliases=["jk","fun"])
