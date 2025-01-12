import os, sys, subprocess
import pyttsx3

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def say_async(text):
    try:
        subprocess.Popen([os.path.join(application_path, 'tts.exe'), text])
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        say(sys.argv[1])
    else:
        say('Привет, мир!')