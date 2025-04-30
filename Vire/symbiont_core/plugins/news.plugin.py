# symbiont_core/plugins/news.plugin.py

import json
import urllib.parse
import urllib.request
from pathlib import Path

def news_cmd(args):
    """
    Fetch top headlines from NewsAPI.
    Usage: news [query]
    Example: news technology
    """
    # load API key
    cfg_path = Path(__file__).resolve().parents[2] / "config" / "settings.json"
    try:
        with open(cfg_path, encoding="utf-8-sig") as cf:
            cfg = json.load(cf)
        key = cfg.get("NEWSAPI_API_KEY")
    except Exception:
        key = None

    if not key:
        print("⚠️  Please set NEWSAPI_API_KEY in config/settings.json")
        return

    query = " ".join(args) if args else ""
    params = {
        "apiKey": key,
        "pageSize": 5
    }
    if query:
        params["q"] = query
    else:
        params["country"] = "us"  # default to US headlines

    qs = urllib.parse.urlencode(params)
    url = f"https://newsapi.org/v2/top-headlines?{qs}"

    try:
        with urllib.request.urlopen(url) as resp:
            data = json.load(resp)
    except Exception as e:
        print(f"⚠️  Error fetching news: {e}")
        return

    status = data.get("status")
    if status != "ok":
        print(f"⚠️  API error: {data.get('message')}")
        return

    articles = data.get("articles", [])
    if not articles:
        print("⚠️  No articles found.")
        return

    print(f"\n📰 Top {len(articles)} headlines for “{query or 'general'}”:")
    for art in articles:
        title = art.get("title")
        src   = art.get("source", {}).get("name")
        print(f" • {title}  ({src})")
    print()

def register(register_command):
    register_command("news", news_cmd, aliases=["headlines"])
