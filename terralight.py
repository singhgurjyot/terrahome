# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 23:43:40 2020

@author: singh
"""

from phue import Bridge

BRIDGE_IP='something'

b = Bridge(BRIDGE_IP)

b.connect()
b.get_api()
b.get_light(1, 'on')
b.set_light(1, 'bri', 254)
b.set_light(2, 'bri', 127)
b.set_light( [1,2], 'on', True)
b.get_light(1, 'name')
b.get_light('Kitchen')
command =  {'transitiontime' : 300, 'on' : True, 'bri' : 254}
b.set_light(1, command)
