import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[0]))

from symbiont_core.symbiont import Symbiont
from symbiont_core.interfaces.cli_interface import launch_cli

if __name__ == '__main__':
    print("Booting Symbiont...")
    s = Symbiont()
    print(s.heartbeat())

    print("\nLaunching CLI...")
    launch_cli()
