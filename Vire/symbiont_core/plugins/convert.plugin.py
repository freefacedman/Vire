# symbiont_core/plugins/convert.plugin.py

import json
import urllib.parse
import urllib.request
from pathlib import Path

def convert_cmd(args):
    """
    Convert an amount from one currency to another.
    Uses exchangerate.host by default (free, no key).
    Falls back to Apilayer Exchange Rates if you set EXCHANGE_API_KEY.
    Usage: convert [amount] [from_currency] [to_currency]
    """
    if len(args) < 3:
        print("Usage: convert [amount] [from_currency] [to_currency]")
        return

    # parse amount
    try:
        amount = float(args[0])
    except ValueError:
        print("⚠️  First argument must be a number.")
        return

    frm = args[1].upper()
    to  = args[2].upper()

    # load config
    cfg_path = Path(__file__).resolve().parents[2] / "config" / "settings.json"
    api_key = None
    if cfg_path.exists():
        try:
            with open(cfg_path, encoding="utf-8-sig") as cf:
                cfg = json.load(cf)
            api_key = cfg.get("EXCHANGE_API_KEY")
        except Exception:
            pass

    # build URL
    if api_key:
        # Apilayer Exchange Rates API (needs key)
        qs = urllib.parse.urlencode({
            "access_key": api_key,
            "from": frm,
            "to": to,
            "amount": amount
        })
        url = f"http://api.exchangeratesapi.io/v1/convert?{qs}"
    else:
        # exchangerate.host free API
        qs = urllib.parse.urlencode({
            "from": frm,
            "to": to,
            "amount": amount
        })
        url = f"https://api.exchangerate.host/convert?{qs}"

    # fetch
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.load(resp)
    except Exception as e:
        print(f"⚠️  Error fetching conversion: {e}")
        return

    # handle Apilayer error format
    if api_key:
        if not data.get("success", False):
            err = data.get("error", {}).get("type", "Unknown error")
            print(f"⚠️  API error: {err}")
            return
        result = data.get("result")
        rate   = (data.get("info") or {}).get("rate")
    else:
        # exchangerate.host always returns result and info.rate
        result = data.get("result")
        rate   = (data.get("info") or {}).get("rate")

    if result is None or rate is None:
        print("⚠️  Conversion data not available.")
        return

    print(f"\n💱 {amount} {frm} = {result:.4f} {to}  "
          f"(1 {frm} = {rate:.4f} {to})\n")

def register(register_command):
    register_command("convert", convert_cmd, aliases=["currency","curr"])
