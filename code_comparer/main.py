"""
Run from this directory: python main.py

Forwards to directory_monitor.py by default (SHA256, JSON, optional --monitor).
Use --basic for directory_compare.py (MD5, lighter output).
"""
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent


def main() -> None:
    os.chdir(_ROOT)
    sys.path.insert(0, str(_ROOT))
    argv = sys.argv[1:]
    if argv[:1] == ["--basic"]:
        import directory_compare

        directory_compare.main()
        return
    import directory_monitor

    sys.argv = [sys.argv[0], *argv]
    directory_monitor.main()


if __name__ == "__main__":
    main()
