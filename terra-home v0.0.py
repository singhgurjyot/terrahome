# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 22:59:10 2020

@author: singh
"""

import speech_recognition as sr
import pyttsx3
from wit import Wit
import time
from core.tokenizer import tokenize


engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[2].id)

WIT_ACCESS_TOKEN = 'HDYAELNDNBUCN7H3SWHCJ4COTEBKUYO2'
intent_classifier = Wit(WIT_ACCESS_TOKEN)

def speechRecognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('> ' + command + '\n')
    except sr.UnknownValueError:
        print("Couldn't understand your command, please say again...")
        engine.say("Couldn't understand your command, please say again...")
        engine.runAndWait()
        time.sleep(0.5)
        command = speechRecognize()
    return command

print("\nHello, Terra Home here your home assistant. How may I help you?")
engine.say("Hello, Terra Home here, your home assistant. How may I help you?")
engine.runAndWait()

listen = True

while listen:
    question = speechRecognize()
    #question = input('> ')
    ques_tokens = tokenize(question)
    
    if 'bye' in ques_tokens or 'goodbye' in ques_tokens or 'see you later' in ques_tokens or 'exit' in ques_tokens:
        system.exit(0)
        
    intent_resp = intent_classifier.message(question)
    
    print(intent_resp)
    
    if 'intent' in intent_resp['entities']:
        intent = intent_resp['entities']['intent'][0]['value']
        
    if 'intent' == 'light':
        if 'room' in intent_resp['entities']:
            room = intent_resp['entities']['room'][0]['value']
        else:
            room = 'bedroom'
            
        on_off = intent_resp['entities']['on_off'][0]['value']
        print(room, on_off)
    
    
    