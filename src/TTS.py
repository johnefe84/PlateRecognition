'''
Created on 20/08/2014

@author: johnefe
'''
import pyttsx3


def hablar(texto):
    #Se inicia el motor de voz
    engine = pyttsx.init()
    engine.setProperty('rate', 100)
    #Se selecciona el idioma a utilizar
    #voices = engine.getProperty('voices')
    #for voice in voices:
    #   print(voice.id)
    #   engine.setProperty('voice', voice.id)
    #engine.setProperty('voice', "spanish-latin-american")
    #Se genera la voz a partir de un texto
    engine.say(texto)
    engine.runAndWait()
    
#hablar("hola")