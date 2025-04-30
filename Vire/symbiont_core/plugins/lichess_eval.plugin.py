# symbiont_core/plugins/lichess_eval.plugin.py

import urllib.parse
import urllib.request
import json

def lichess_cmd(args):
    """
    Get a best‐move and evaluation from Lichess Cloud Analysis.
    Usage: lichess [FEN] [multiPv] [depth]
    Examples:
      lichess                            → starting position, 1 top move, depth=15
      lichess <FEN> 3 20                → custom FEN, 3 candidate moves, depth=20
    """
    # defaults
    fen     = args[0] if args else "startpos"
    multipv = int(args[1]) if len(args)>1 and args[1].isdigit() else 1
    depth   = int(args[2]) if len(args)>2 and args[2].isdigit() else 15

    # for starting position, Lichess wants the FEN string:
    if fen.lower() == "startpos":
        fen = "rn1qkbnr/ppp1pppp/8/3p4/3P4/5N2/PPP1PPPP/RNBQKB1R w KQkq - 0 1"  # or use standard start FEN

    # build URL
    params = {
        "fen":     fen,
        "multiPv": multipv,
        "depth":   depth
    }
    url = "https://lichess.org/api/cloud-eval?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
    except Exception as e:
        print(f"⚠️  Cloud analysis failed: {e}")
        return

    if "error" in data:
        print(f"⚠️  API error: {data['error']}")
        return

    # data["pvs"] is a list of PV objects
    print(f"\n☁️  Lichess Cloud Eval (depth={depth}, multiPv={multipv}):")
    for pv in data.get("pvs", []):
        move   = pv.get("moves", "").split()[0]
        score  = pv.get("cp")  # centipawn
        mate   = pv.get("mate")  # mate in N
        sd     = pv.get("sd")  # search depth reported
        evalstr = f"{score/100:.2f}" if score is not None else f"mate in {mate}"
        print(f" • Move: {move}    Eval: {evalstr}    Depth reported: {sd}")
    print()

def register(register_command):
    register_command("lichess", lichess_cmd,
                     aliases=["cloud","eval"])
