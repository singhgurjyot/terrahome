# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:10:47 2019

@author: singh
"""

import webbrowser
import requests
import bs4 as bs
import smtplib
import pandas as pd
import random
import pyowm


CLIENT_ID = 'RWINEW5YS0D3ONXTR4G1RPH2PAEQRTNFWMSFA001KFW1LGSB'
CLIENT_SECRET = 'QQYGBVSIM1YSVXAO3ENP4NN2VJKIDICEKJSLWICYW0RDGPQ3'
VERSION = '20180605'
WEATHER_API_KEY = 'f250f3234def773eaea5e2faebcc2015'
LOCATION_API_KEY = 'fc1c4737a09587cede833b86ae952973'

degree_sign= u'\N{DEGREE SIGN}'


def play_music(song, artist, movie):
    youtube = 'https://www.youtube.com'
    
    if song == '' and artist == '' and movie == '':
        song = "god's plan"
    
    tokens=[]
    
    tokens.extend(song.split(' '))
    
    if artist != '':
        if song != '':
            tokens.append('by')
        tokens.extend(artist.split(' '))
        
    if movie != '':
        if song != '':
            tokens.append("from")
        tokens.extend(movie.split(' '))
    
    full_qry = ' '.join(tokens)
    qry = '+'.join(tokens)
    url = youtube+'/results?search_query='+qry
    #try:
    res = requests.get(url)
    soup = bs.BeautifulSoup(res.text, 'lxml')
    vids = []
    for link in soup.select('.yt-uix-tile-link'):
        vids.append(link.get('href'))
    webbrowser.open(youtube+vids[0])
    return("Playing "+full_qry+" on Youtube.")
        
        
    #except:
        #return("Cannot open YouTube, Please Check your Internet Connection or try again later.")
        
        
def send_email(email_id='singh.gurjyot08@gmail.com', body='Hi Gurjyot, This is a mail from terrabot'):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('terrabotofficial@gmail.com', 'terrabotisthebest')
        server.sendmail('terrabotofficial@gmail.com', email_id, body)
        server.close()
        return("Email sent to "+email_id)
    except:
        return("Unable to send email, Please Check your Internet Connection or try again later.")
    
    
def get_nearby_venues(name, lat, long, radius=500, LIMIT=15):
    venues_list = []
    url = "https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}".format(
    CLIENT_ID,
    CLIENT_SECRET,
    VERSION,
    lat, long,
    radius,
    LIMIT)
    
    try:
        results = requests.get(url).json()['response']['groups'][0]['items']
        venues_list.append([(
                v['venue']['name'],
                v['venue']['location']['lat'],
                v['venue']['location']['lng'],
                v['venue']['categories'][0]['name']) for v in results])

        nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
        nearby_venues.columns=['shop_name', 'lat', 'long', 'category']    
        return nearby_venues
    except:
        err = "Cannot find places right now, Please Check your Internet Connection or try again later."
        return err
 
    
def get_joke():
    with open('jokes.txt', 'r') as f:
        jokes = f.readlines()
        joke = random.choice(jokes)
        ques, ans = joke.split('~')
    return(ques, ans)

def weather_forecast(state='Delhi'):
    try:
        owm = pyowm.OWM(WEATHER_API_KEY)
        obs = owm.weather_at_place('{}'.format(state))
        weather = obs.get_weather()
        temp = weather.get_temperature('celsius')['temp']
        return('The temperature in '+state+" is "+str(temp)+degree_sign+"C.")
    except:
        return("Unable to find temperature right now, Please Check your Internet Connection or try again later.")
    
def goodbye():
    with open('greetings_bye.txt', 'r') as f:
        greetings = f.readlines()
        result = random.choice(greetings)
    return result
