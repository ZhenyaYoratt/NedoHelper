import os

os.system('pip install -r requirements.txt --upgrade')

os.system('python -m ensurepip --upgrade')
os.system('python -m pip install --upgrade setuptools')

os.system('pyinstaller .\modules\tts.py --onefile')
os.system('pyinstaller main.py --onefile -n NedoHelper --add-data dist:tts.exe')
os.system('pyinstaller installer.py --onefile --add-data dist:NedoHelper.exe')
