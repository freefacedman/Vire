# symbiont_core/plugins/stockfish.plugin.py

import json
from pathlib import Path
import urllib.request
import chess
import chess.engine

def stockfish_cmd(args):
    """
    Ask Stockfish for the best move.
    Usage:
      stockfish [FEN] [depth]
    Examples:
      stockfish             → starting‐position, depth=15
      stockfish <FEN> 20    → custom position, depth=20
    """
    # load stockfish path
    cfg_path = Path(__file__).resolve().parents[2] / "config" / "settings.json"
    try:
        with open(cfg_path, encoding="utf-8-sig") as cf:
            keycfg = json.load(cf)
        sf_path = keycfg.get("STOCKFISH_PATH", "stockfish")
    except Exception:
        sf_path = "stockfish"

    # default to starting position
    if args and args[0].isdigit() is False and len(args) >= 1:
        # first arg isn’t a number → treat as FEN
        fen = args[0]
        depth = int(args[1]) if len(args) > 1 and args[1].isdigit() else 15
    else:
        fen = chess.STARTING_FEN
        depth = int(args[0]) if args and args[0].isdigit() else 15

    try:
        engine = chess.engine.SimpleEngine.popen_uci(sf_path)
    except FileNotFoundError:
        print(f"⚠️  Stockfish binary not found at '{sf_path}'.")
        return
    except Exception as e:
        print(f"⚠️  Error launching Stockfish: {e}")
        return

    board = chess.Board(fen)
    print(f"\n♟️  Position: {'starting' if fen==chess.STARTING_FEN else 'custom FEN'}")
    print("   " + board.unicode(borders=True))

    # ask for best move
    try:
        info = engine.analyse(board, chess.engine.Limit(depth=depth))
        best = info.get("pv", [None])[0]
        score = info.get("score")
    except Exception as e:
        print(f"⚠️  Engine analysis failed: {e}")
        engine.quit()
        return

    engine.quit()

    if best is None:
        print("⚠️  Could not find a best move.")
        return

    print(f"\n✅ Best move at depth {depth}: {best.uci()}")
    if score:
        print(f"   Evaluation: {score}\n")
    else:
        print()

def register(register_command):
    register_command("stockfish", stockfish_cmd,
                     aliases=["sf", "bestmove"])
