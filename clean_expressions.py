# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:22:18 2020

@author: singh
"""

with open("expressions-1.json", 'r') as f:
    data = f.read()
    
data = data.replace('\\"', '')\

with open("expressions-1.json", 'w') as f:
    f.write(data)