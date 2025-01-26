import os
print('Installing requirements...')
os.system('pip install -r requirements.txt --upgrade')
print('Upgrading python tools...')
os.system('python -m ensurepip --upgrade')
os.system('python -m pip install --upgrade setuptools')
print('Starting building...')
os.system('pyinstaller .\modules\tts.py --onefile --windowed')
os.system('pyinstaller main.py --onefile -n NedoHelper --add-data dist:tts.exe --windowed --uac-admin')
#os.system('pyinstaller installer.py --onefile --add-data dist:NedoHelper.exe --windowed')

print("""
    Done!
""")