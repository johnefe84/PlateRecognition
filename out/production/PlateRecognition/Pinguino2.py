'''
Created on 4/09/2014

@author: johnefe
'''

from pynguino import PynguinoUSB
import time

p = PynguinoUSB("v2") #bootloaderV2  
p.write("r")
'''
while True:
    p.write("AbcDEF")
    time.sleep(10)
    p.write("aBcDEF")
    time.sleep(10)
    p.write("abCDEF")
    time.sleep(10)
    p.write("abcDEF")
    time.sleep(10)
'''

    

