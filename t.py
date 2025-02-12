# translate.py
"""
To translate the program, simply run:

    py t.py

    python t.py
    python.exe t.py
    python3.exe t.py

"""
from os import system
files_list = [
    r'.\ui\about.py',
    r'.\ui\antivirus.py',
    r'.\ui\browser.py',
    r'.\ui\desktop_manager.py',
    r'.\ui\disk_manager.py',
    r'.\ui\settings.py',
    r'.\ui\software_launcher.py',
    r'.\ui\system_restore.py',
    r'.\ui\task_manager.py',
    r'.\ui\unlocker.py',
    r'.\ui\user_manager.py',
]
l = ' '.join(files_list)
cmd = "pylupdate5 main.py " + l + r" -ts .\localizations\en.ts"
system(cmd)
print('✅ The translation file has been updated!')
print("didn't ask.")