"""Run PyInstaller to create a binary."""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "artist.py")

def install()->None:
    """Install Function to build binary with pyInstaller."""
    command = [
        "pyinstaller",
        path_to_main,
        "--onefile",
        "--clean",
        "--hidden-import=epics.clibs",
        # other pyinstaller options...
    ]
    subprocess.run(command, check=True)

