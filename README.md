# YoHelper ![GitHub last commit](https://img.shields.io/github/last-commit/ZhenyaYoratt/YoHelper?style=flat-square) ![GitHub License](https://img.shields.io/github/license/ZhenyaYoratt/YoHelper?style=flat-square) ![GitHub top language](https://img.shields.io/github/languages/top/ZhenyaYoratt/YoHelper?style=flat-square)

![Image of YoHelper](/docs/images/main_window.png)

The multitool program will allow you to remove viruses (may be) and restore Windows 10 to its perfect state. This program is designed exclusively for [the YouTube channel "NEDOHACKERS Lite"](https://youtube.com/@nedohackerslite).

![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/ZhenyaYoratt/YoHelper/latest/total?style=for-the-badge&logo=github) ![GitHub file size in bytes](https://img.shields.io/github/size/ZhenyaYoratt/YoHelper/main.py)

> [!CAUTION]
> This program needs to be improved to its ideal state. **Use it AT <ins>YOUR OWN RISK AND RISK</ins>, test it ONLY ON VIRTUAL MACHINES.** If you find problems, feel free to [create a Issue](/issues) and describe it!
> 
> ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/ZhenyaYoratt/YoHelper?style=flat-square)

> [!IMPORTANT]
> This program is developed in Russian, but it does not yet have an international translation, including English. Please be patient!

## Download
Download [the lastest release version](https://github.com/ZhenyaYoratt/YoHelper/releases) of the program. There are also file hashes and links to antivirus scans.
[![VirusTotal results](https://img.shields.io/badge/VirusTotal-blue?style=flat-square)](https://virustotal.com)
<!-- VirusTotal/Trag.le -->

## Features
The following features are built into the program:
- Antivirus
- Browser
- Desktop Manager
- Disk Manager
- Software Launcher
- System Restore
- Task Manager
- User Manager

## Known issues
- The process type (Task Manager) are not displayed correctly.
- The program freezes while scanning the folder for viruses.
<!-- There are no issues at the moment. If you find problems, feel free to [create a Issue](github.com/ZhenyaYoratt/YoHelper/issues) and describe it.-->

## TODO
- [ ] Add external authorization to NedoTube account
- [ ] Translate program to English (i18n)

## Build
To build the program, just run this command:
```
python build.py
```
Or without using python:
```
pip install -r requirements.txt --upgrade

python -m ensurepip --upgrade
python -m pip install --upgrade setuptools

pyinstaller .\modules\tts.py --onefile
pyinstaller main.py --onefile -n NedoHelper --add-data dist:tts.exe
pyinstaller installer.py --onefile --add-data dist:NedoHelper.exe
```
> [!NOTE]
> You need to have the following dependencies installed before running without using python.


## Contributing Guidelines
Please ensure to adhere to the coding standards and include comments where necessary. For larger changes, it's recommended to open an issue first to discuss potential alterations.

## Dependencies Used
- `Python` 3.11.9
- `PyQt5` 5.15.11
- `PyQtWebEngine` 5.15

See the full list in the file [requirements.txt](requirements.txt).

## Acknowledgments
Special thanks to the open-source community for providing libraries and tools that facilitate rapid development. This project leverages several community resources to enhance its functionality.

## License
This project is licensed under the terms of GNU General Public License version 3.0 or newer. You can see full license text in [LICENSE](LICENSE) file.

## Star History
<a href="https://star-history.com/#ZhenyaYoratt/YoHelper&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ZhenyaYoratt/YoHelper&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ZhenyaYoratt/YoHelper&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ZhenyaYoratt/YoHelper&type=Date" />
 </picture>
</a>

---

Feel free to reach out to the repository owner, [ZhenyaYoratt](https://github.com/ZhenyaYoratt), for any questions or guidance regarding the project.
