import win32com.client
import speech_recognition as sr
import webbrowser
import os
import datetime
import subprocess
import pyautogui
import time


def speak(text):
    print(text)
    if len(text)<100:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)

def take_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listenning...")

        try:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            print("Recognizing...")
            mytext = r.recognize_google(audio, language="en-in")
            mytext = mytext.lower()
            # speak(f"You said: {mytext}")
            print(f"You said: {mytext}")

        except Exception as e:
            print(e)

        return mytext
    
if __name__ == "__main__":
    speak("Hello sir. I am Jarvis.")
   
    while True: 
        try:
            mytex = take_voice()
        except:
            speak("Please say again sir.")
            continue

        if "open web" in mytex:
            sites = [["youtube", "https://www.youtube.com/"], ["google", "https://www.google.com/"], ["wikipedia", "https://www.wikipedia.com/"]]

            for site in sites: # it run until it not in mytex
                if f"open web {site[0]}" in mytex:
                    speak(f"{site[0]} is openning...")
                    webbrowser.open(site[1])
            continue

        if "play music" in mytex:
            s = ["downfall", "sound"]
            for song in s: # it run until it not in mytex
                if f"play music {song}" in mytex:
                    music_path = f"C:/Users/Windows/Music/{song}.mp3"
                    os.startfile(music_path)
            continue

        if "the time" in mytex:
            strftime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strftime}")
            continue

        if "open notepad" in mytex:
            speak("openning...")
            subprocess.Popen("C:/Users/Windows/Desktop/mynotepad.exe")
            continue

        if "open edge" in mytex:
            speak("openning...")

            subprocess.Popen("start msedge", shell=True)

            time.sleep(2)

            pyautogui.hotkey('ctrl', 'space')
            exit()
            continue

        t = ["exit", "bye", "goodbye"]
        for i in t:
            if i in mytex:
                speak("Thanks for giving a time sir.")
                exit()