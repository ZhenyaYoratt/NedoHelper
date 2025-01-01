@echo off

pip install -r requirements.txt --upgrade

python -m ensurepip --upgrade
python -m pip install --upgrade setuptools

pyinstaller main.py --onefile -n NedoHelper
pyinstaller installer.py --onefile --add-data dist:NedoHelper.exe
