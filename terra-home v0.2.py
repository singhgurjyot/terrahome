# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 17:56:35 2019

@author: singh

"""
from wit import Wit
import speech_recognition as sr
import moddedinference as chatbot
import colorama
import scoring
import random
import time
import features
from core.tokenizer import tokenize
import requests
import json
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


ACCESS_TOKEN = '3GQB7F5MUXZW6NRWBTSZWEWAIPM5BO74'
intent_classifier = Wit(ACCESS_TOKEN)
url = "https://api.wit.ai/message?v=20201005&q="
"""
play = False

def listening():
    animation = "|/-\\"
    idx = 0
    while play:
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
"""


def myCommand():
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
        command = myCommand()
    return command


print("\nHello, Terra Home here your home assistant. How may I help you?")
engine.say("Hello, Terra Home here, your home assistant. How may I help you?")
engine.runAndWait()
colorama.init()

listen = True

intents = ['song', 'email', 'weather', 'foursquare_explore', 'joke', 'bye', '"light"']
# QAs
while listen:
    question = myCommand()
    #question = input('> ')
    ques_tokens = tokenize(question)
    #try:
    #intent_resp = intent_classifier.message(question)
    resp = requests.get(url+question, headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
    intent_resp = json.loads(resp.text)
    intent_resp_str = resp.text


    
    
    if len(intent_resp['intents']) > 0:
        intent = intent_resp['intents'][0]['name'].replace('"', "")
    else:
        intent = 'chat'
    
    if intent not in intents:
        intent = 'chat'
        
    if 'bye' in ques_tokens or 'goodbye' in ques_tokens or 'see you later' in ques_tokens or 'exit' in ques_tokens:
        intent = 'bye'
        
    if intent == 'light':
        if 'room:room' in intent_resp['entities']:
            room = intent_resp['entities']['room:room'][0]['value']
        else:
            room = 'bedroom'
            
        on_off = intent_resp['traits']['wit$on_off'][0]['value']
        print(room, on_off)
    
    
    elif intent == 'song':
        if 'songname:songname' in intent_resp['entities']:
            song_name = intent_resp['entities']['songname:songname'][0]['value'].replace('"', "")
        else:
            song_name = ''
        if 'songartist:songartist' in intent_resp['entities']:
            song_artist = intent_resp['entities']['songartist:songartist'][0]['value'].replace('"', "")
        else:
            song_artist = ''
        if 'songmovie:songmovie' in intent_resp['entities']:
            song_movie = intent_resp['entities']['songmovie:songmovie'][0]['value'].replace('"', "")
        else:
            song_movie = ''
        
        response = features.play_music(song_name, song_artist, song_movie)
        print(response)
        engine.say(response)
        engine.runAndWait()
    
    elif intent == 'email':
        if 'email' in intent_resp['entities']:
            email_id = intent_resp['entities']['email'][0]['value']
        else:
            engine.say("Who is the reciever?")
            engine.runAndWait()
            email_id = input("Enter the receivers Email ID: ")
            
            
        if 'message_body' in intent_resp['entities']:
            msg = intent_resp['entities']['message_body'][0]['value']
        else:
            engine.say("What should I say?")
            engine.runAndWait()
            msg = input("Enter the message body: ")
            
        
        response = features.send_email(email_id=email_id, body=msg)
        print(response)
        engine.say(response)
        engine.runAndWait()
        
    elif intent == 'weather':
        if 'wit$datetime:datetime' in intent_resp['entities']:
            date_ = intent_resp['entities']['wit$datetime:datetime'][0]['value']
            date_ = date_[:10]
        else:
            date_ = None
        if 'location' in intent_resp['entities']:
            loc = intent_resp['entities']['location'][0]['resolved']['values'][0]['name']
        else:
            loc = 'Delhi'
            
        forecast = features.weather_forecast(loc)
        
        print(forecast)
        engine.say(forecast)
        engine.runAndWait()
        
        
    elif intent == 'foursquare_explore':
        if 'location' in intent_resp['entities']:
            if 'resolved' in intent_resp['entities']['location'][0]:
                location = intent_resp['entities']['location'][0]['resolved']['values'][0]['name']
                lat = intent_resp['entities']['location'][0]['resolved']['values'][0]['coords']['lat']
                lng = intent_resp['entities']['location'][0]['resolved']['values'][0]['coords']['long']
                
        else:
            geo_req = requests.get("http://api.ipstack.com/check?access_key={}".format(features.LOCATION_API_KEY))
            geo_json = json.loads(geo_req.text)
            location = geo_json['city']
            lat = geo_json['latitude']
            lng = geo_json['longitude']
            
        print(features.get_nearby_venues(location, lat, lng))
        engine.say("Here you go")
        engine.runAndWait()
        
    elif intent == 'joke':
        ques, ans = features.get_joke()
        print(ques)
        engine.say(ques)
        engine.runAndWait()
        time.sleep(3)
        print(ans)
        engine.say(ans)
        engine.runAndWait()
        
    elif intent == 'chat':
        answers, answers_rate = chatbot.inference_internal(question)
        ans_score = {}
        for i, answer in enumerate(answers):
            score = scoring.do_scoring(question, answer, answers_rate[i])
            ans_score[answer] = score
        scores = [v for k,v in ans_score.items()]
        max_score = max(scores)
        options = [k for k,v in ans_score.items() if v == max_score]
        choice_answer = random.choice(options)
        print("{}TerraBot: {}{}".format(colorama.Fore.GREEN, choice_answer, colorama.Fore.RESET))
        engine.say(choice_answer)
        engine.runAndWait()
        
    elif intent == 'bye':
        bye = features.goodbye()
        print(bye)
        engine.say(bye)
        engine.runAndWait()
        listen = False
    #except:
        #print("Please Check your Internet Connection or try again later.")
    
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            