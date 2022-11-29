import webbrowser
import playsound
from gtts  import gTTS
from flask import Flask,render_template,request,redirect,url_for,jsonify,Blueprint
import random
import os
import speech_recognition as spr 
import time

import pymongo

recog=spr.Recognizer()
client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb=client['User_info']
reminder_collection=mydb.reminder


def speak(answer):
    tts=gTTS(text=answer,lang='en')
    r=random.randint(1,100000)
    file_name='audio-'+str(r)+'.mp3'
    tts.save(file_name)
    playsound.playsound(file_name)
    print(file_name)
    os.remove(file_name)

def record_voice():
    with spr.Microphone() as source:
        
        voice=''
        try:
            command=recog.listen(source)
            voice=recog.recognize_google(command)
        except spr.UnknownValueError:
            speak("Sorry, I did'nt get you please speak clearly")
            
        except spr.RequestError:
            speak('sorry , i am not working right now')
            
        return voice

def respond(voice):
    val=[1,'null']
    if(voice==''):
        return val
    if 'your name' in voice:
        answer="my name is one and two"
        speak(answer)
        
    elif 'current time' in voice:
        answer=time.ctime()
        speak(answer)
    elif 'search' in voice:
        speak('what do you want to search for')
        voice1=record_voice() 
        url='https://google.com/search?q='+voice1
        webbrowser.get().open(url)
        speak('This is what i found for '+ voice1)
    elif 'exit' in voice:
        speak(' Ok Bye')
        val[0]=0
        # exit()
        
    elif '121' in voice:
        print("notes")
        speak('Note Down')
        val[0]=0
        val[1]='notes.html'

        
    elif '131' in voice:
        print('remainder')
        speak('Remind me')
        val[0]=0
        val[1]='remainder.html'
    elif 'make n' in voice:
        print('make notes')
        speak('Remind me')
        val[0]=0
        val[1]='remainder.html'
    else:
        speak('Sorry but i am still learning this')
    return val

def record_notes():
    speak('Please speak in this format')
    speak('first Title')
    speak('And then Text')
    with spr.Microphone() as source:
        
        voice=''
        try:
            command=recog.listen(source)
            voice=recog.recognize_google(command)
        except spr.UnknownValueError:
            speak("Sorry, I did'nt get you please speak clearly")
            
        except spr.RequestError:
            speak('sorry , i am not working right now')
            
        return voice

def response_notes(voice):
    val=[1,'null']
    
    print(voice)
    speak(voice)
    speak('Note added successfully')
    val[1]=voice
    val[0]=0
    return val

def record_rem():
    while 1:
        with spr.Microphone() as source:
            
            voice=''
            try:
                command=recog.listen(source)
                voice=recog.recognize_google(command)
            except spr.UnknownValueError:
                speak("Sorry, I did'nt get you please speak clearly")
                
            except spr.RequestError:
                speak('sorry , i am not working right now')

                
            return voice
            

    


def shownotes():
    return redirect('/dashboard/notes')

def showReminder():
    return redirect('/showReminder')