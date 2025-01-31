import sys
from os import path
from subprocess import Popen
from pyttsx3 import init

if getattr(sys, 'frozen', False):
    application_path = path.dirname(sys.executable)
elif __file__:
    application_path = path.dirname(__file__)

def say(text):
    engine = init()
    engine.say(text)
    engine.runAndWait()

def say_async(text):
    try:
        Popen([path.join(application_path, 'tts.exe'), text])
    except Exception as e:
        pass#print(f'Error: {e}')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        say(sys.argv[1])
    else:
        say('Привет, мир!')