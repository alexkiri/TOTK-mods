import platform
import subprocess
from configuration.settings import *
latest_version = Version.strip("manager-")


if __name__ == "__main__":
    if platform.system() == "Windows":
        command = [
            "pyinstaller",
            "run.py",
            "--onefile",
            f"--name=TOTK_Optimizer_{latest_version}",
            "--add-data", "GUI;GUI",
            "--add-data", "json.data;json.data"
        ]
        subprocess.run(command, shell=True)
        
    if platform.system() == "Linux":
        command = [
            "pyinstaller",
            "--onefile",
            "--collect-all", "ttkbootstrap",
            f"--name=TOTK Optimizer {latest_version}.AppImage",
            "run.py",
            "--add-data", "GUI:GUI",
            "--add-data", "json.data:json.data"
            "--hidden-import=PIL",
            "--hidden-import=PIL._tkinter_finder",
            "--hidden-import=PIL._tkinter",
            "--hidden-import=ttkbootstrap",
        ]
        subprocess.run(command, check=True)
