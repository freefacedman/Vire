# Vire / Symbiont

An extensible AI companion that learns, reflects, and simulates from user-provided inputs. It supports:

- **Memory Management**: summaries, reflections, reflection tree growth, tag-based search
- **Live Chat CLI**: interactive conversation shell with commands
- **Plugins**: easily add new capabilities via `symbiont_core/plugins/*.plugin.py`

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://your.repo.url/Vire.git
   cd Vire
   ```
2. **Ensure Python 3.8+ is installed**.
3. **Install any dependencies** (if needed):
   > _By default, uses only the standard library for plugins and chat._
4. **Create your config**:
   ```json
   {
     "learning_rate": 0.10,
     "reflection_interval_minutes": 30,
     "model": "VIRE",
     "logging": {
       "level": "INFO",
       "file": "logs/activity.log"
     },
     "OPENWEATHER_API_KEY": "YOUR_OPENWEATHERMAP_KEY_HERE",
     "NEWSAPI_API_KEY": "YOUR_NEWSAPI_KEY_HERE",
     "EXCHANGE_API_KEY": "YOUR_EXCHANGE_API_KEY_HERE"
   }
   ```
   Save as `config/settings.json` (UTF-8 without BOM).

---

## 🚀 Usage

Run the live chat:
```bash
python training_pipeline/live_chat.py
```

Type any of the commands below at the `You>` prompt.

---

## 💬 Commands Reference

| Command                                   | Aliases               | Description                                         |
|-------------------------------------------|-----------------------|-----------------------------------------------------|
| `search [tag]`                            | `s`, `se`             | List summaries & reflections matching a tag         |
| `tree [tag] [layers=2]`                   | `t`, `tr`             | Build a multi-layer reflection tree                 |
| `simulate [text] [layers=3]`              | `sim`                 | What-if scenario simulation                         |
| `wiki [topic]`                            | `w`, `define`         | Fetch Wikipedia summary                             |
| `weather [city,country]`                  | `wthr`                | Current weather via OpenWeatherMap                  |
| `news [query]`                            | `headlines`           | Top headlines via NewsAPI                           |
| `define [word]`                           | `dict`, `def`         | Dictionary definitions (dictionaryapi.dev)          |
| `translate [text] [lang_code]`            | `trans`               | Translate text via LibreTranslate                   |
| `joke`                                    | `jk`, `fun`           | Random joke from Official Joke API                  |
| `crypto [coin_id] [vs_currency]`          | `cg`, `coin`          | Cryptocurrency price from CoinGecko                 |
| `convert [amt] [from] [to]`               | `currency`, `curr`    | Currency conversion via exchangerate.host / fallback|
| `metrics`                                 | `stats`, `m`          | Show counts & tag frequencies in memory             |
| `help`                                    | `h`, `?`              | Show this command list                              |
| `exit`                                    | `q`, `quit`           | Exit the chat                                       |

---

## 🧩 Plugins

Drop any `*.plugin.py` into `symbiont_core/plugins/`, and it will be auto-loaded. Each plugin must define:

```python
# example.plugin.py

def register(register_command):
    register_command("cmd_name", func, aliases=[...])
```

Existing plugins include:

- **wiki**: Wikipedia summaries
- **weather**: OpenWeatherMap current conditions
- **news**: NewsAPI headlines
- **define**: Dictionary definitions
- **translate**: Text translation
- **joke**: Random jokes
- **crypto**: CoinGecko prices
- **convert**: Currency conversion
- **metrics**: Memory metrics

---

## 🛠 Development & Testing

- **Ingest** new inputs: `python training_pipeline/ingest.py`
- **Run tests** (pytest):
  ```bash
  pytest -q
  ```
- **Logs** are written to: `logs/activity.log`, `logs/changes.log`

---

Happy symbiosis! 🌱

