# symbiont_core/plugins/weather.plugin.py

import json
import urllib.parse
import urllib.request
from pathlib import Path

def weather_cmd(args):
    """
    Get current weather from OpenWeatherMap.
    Usage: weather [city],[country_code]
    Example: weather London,uk
    """
    if not args:
        print("Usage: weather [city],[country_code]")
        return

    # load API key
    cfg_path = Path(__file__).resolve().parents[2] / "config" / "settings.json"
    try:
        with open(cfg_path, encoding="utf-8-sig") as cf:
            cfg = json.load(cf)
        key = cfg.get("OPENWEATHER_API_KEY")
    except Exception:
        key = None

    if not key:
        print("⚠️  Please set OPENWEATHER_API_KEY in config/settings.json")
        return

    location = args[0]
    q = urllib.parse.quote(location)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={q}&appid={key}&units=metric"

    try:
        with urllib.request.urlopen(url) as resp:
            data = json.load(resp)
    except Exception as e:
        print(f"⚠️  Error fetching weather: {e}")
        return

    if data.get("cod") != 200:
        print(f"⚠️  API error: {data.get('message')}")
        return

    name   = data["name"]
    main   = data["weather"][0]["description"].capitalize()
    temp   = data["main"]["temp"]
    feels  = data["main"]["feels_like"]
    hum    = data["main"]["humidity"]
    print(f"\n☁️  Weather in {name}: {main}")
    print(f"   🌡  Temp: {temp}°C (feels like {feels}°C)")
    print(f"   💧  Humidity: {hum}%\n")

def register(register_command):
    register_command("weather", weather_cmd, aliases=["wthr"])
