import json, pathlib, datetime

CFG = pathlib.Path(__file__).resolve().parents[1] / 'config'

class Symbiont:
    def __init__(self):
        with open(CFG/'identity_schema.json', encoding='utf-8-sig') as f:
            self.identity = json.load(f)
    def heartbeat(self):
        now = datetime.datetime.utcnow().isoformat(timespec='seconds')
        return f"[{now}] Hello, I am {self.identity['name']} and I am alive."

if __name__ == '__main__':
    print(Symbiont().heartbeat())

