# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:40:04 2020

@author: singh
"""

import requests
import json

with open('expressions-1.json', 'r') as f:
    samples = json.load(f)
    
samples = samples['data']

sample = samples[150:]

header = {
      'Authorization': 'Bearer Z33N4HUGYYGDQMQDFJSQIUR5HJP65P26',
      'Content-Type': 'application/json',
    }
res = requests.post('https://api.wit.ai/samples?v=20200420', headers = header, data = json.dumps(sample))

print(res)

print(samples[150])