# symbiont_core/plugins/crypto.plugin.py

import urllib.parse
import urllib.request
import json

def crypto_cmd(args):
    """
    Fetch the current price of a cryptocurrency via CoinGecko.
    Usage: crypto [coin_id] [vs_currency]
    Example: crypto bitcoin usd
    """
    if not args:
        print("Usage: crypto [coin_id] [vs_currency]")
        return

    coin = args[0].lower()
    vs = args[1].lower() if len(args) > 1 else "usd"

    qs = urllib.parse.urlencode({
        "ids": coin,
        "vs_currencies": vs
    })
    url = f"https://api.coingecko.com/api/v3/simple/price?{qs}"

    try:
        with urllib.request.urlopen(url) as resp:
            if resp.status != 200:
                print(f"⚠️  API error: HTTP {resp.status}")
                return
            data = json.load(resp)
    except Exception as e:
        print(f"⚠️  Error fetching price: {e}")
        return

    price_info = data.get(coin)
    if not price_info or vs not in price_info:
        print(f"⚠️  No data for '{coin}' in '{vs}'")
        return

    price = price_info[vs]
    print(f"\n💱 {coin.capitalize()} → {vs.upper()}: {price}\n")

def register(register_command):
    register_command("crypto", crypto_cmd, aliases=["cg", "coin"])
