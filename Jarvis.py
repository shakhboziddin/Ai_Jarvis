# Голосовой ассистент Jarvis 1.0 BETA
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# настройки
opts = {
    "alias": ('jarvis','jarves','jervis','jarvi',),
    "tbr": ('tell','show','how'),
    "cmds": {
        "ctime": ('current time','now is the time','what time is it now'),
        "greating": ('hello', 'hi'),
        "stupid1": ('tell a joke','make me laugh','you know jokes'),
        "here": ('джарвис ты здесь', 'где ты', 'джарвис')
    }
}

# функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Recognized: " + voice)
    
        if voice.startswith(opts["alias"]):
            # обращаются к jarvis
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd) 
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Voice not recognized!")
    except sr.RequestError as e:
        print("[log] Unknown error, check the internet!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    return RC

def execute_cmd(cmd):   
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Now: " + str(now.hour) + ":" + str(now.minute))
    
    elif cmd == 'greating':
        # приветствие
        speak('hello')
    
    elif cmd == 'stupid1':
        # рассказать анекдот
        speak('My developer didn`t teach me jokes... Ha ha ha')    
    elif cmd == 'here':
        speak('да,я здесь!')
    else:
        print('Command not recognized, please try again!')

# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 2)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если у вас установлены голоса для синтеза речи!
#voices = speak_engine.getProperty('voices')
#speak_engine.setProperty('voice', voices[1].id)

# forced cmd test

speak("hello")
speak("I am your voice assistant")
print("I hearing:") 

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop