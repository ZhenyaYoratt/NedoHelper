@echo off

pip install -r requirements.txt -U

pyinstaller main.py --onefile -n NedoHelper
pyinstaller installer.py --onefile --add-data dist:NedoHelper.exe
