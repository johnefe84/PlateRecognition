'''
Created on 20/08/2014

@author: johnefe
'''
import cv2
import urllib 
import numpy as np
import Segmentacion

stream=urllib.urlopen('http://192.168.0.6:8080/video')
bytes=''
continuar=True

while continuar:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        orig_img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        #orig_img =cv2.cvtColor(orig_img,cv2.COLOR_BGR2GRAY)
        #tam=orig_img.shape
        #ancho=tam[0]
        #alto=tam[1]
        #resultado, orig_img2, colorDetectado, tiempoProcesamiento1 = Segmentacion.Segmentar(orig_img,ancho,alto)
        cv2.imshow('i',orig_img)
        cv2.waitKey(10)
        #continuar=False