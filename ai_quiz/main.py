"""
Entry point for the AI Quiz Streamlit app.
Run from this directory: python main.py
"""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    app_script = root / "streamlit-quiz-app.py"
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_script)],
        cwd=str(root),
        check=False,
    )


if __name__ == "__main__":
    main()
