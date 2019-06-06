#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import os
import subprocess
import time
from time import ctime
import speech_recognition as sr
from gtts import gTTS

import webbrowser

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang="en")
    tts.save("audio.mp3")
    return_code = subprocess.call(["afplay", "audio.mp3"])



def activater():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("waiting")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if "please" in data or "Please" in data:
        str.replace(data,data[7:])
    return data


def searchGoogle(data):
    data = data.split(" ")
    if "Google" in data and len(data):
        thingToSearch = "-".join(data[1:])
    elif "up" in data:
        thingToSearch = "-".join(data[2:])
    elif "Search" in data or "search" in data:
        thingToSearch = "-".join(data[1:])
    else:
        thingToSearch = ""

    print("thingtoSearch = " + thingToSearch)
    if thingToSearch != "":
        url = 'http://google.com/#q=' + thingToSearch
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        webbrowser.get(chrome_path).open(url)


commands = {
        "how are you": "I am fine",
        "tell me your name": "my name is Dolores",
        "what is your name": "my name is Dolores",
        "what time is it": ctime(),
        "what is the time": ctime(),
        "tell me the time": ctime(),
        "Search": "Opening Chrome...",
        "Google": "Opening Chrome...",
}


def dolores(data):
        for command in commands:
            if command in data:
                speak(commands[command])
                if "Search" in data or "search" in data or "Google" in data or "up" in datajj:
                    searchGoogle(data)

        if data == "":
            speak("I'm sorry i couldn't hear you")
        if "shut down" in data or "exit" in data or "shutdown" in data or "quit" in data:
            speak("shutting down...")
            exit()


# initialization
time.sleep(2)
speak("Hi. I'm Dolores")
while 1:
        if "Dolores" in activater():
            data = recordAudio()
            dolores(data)
