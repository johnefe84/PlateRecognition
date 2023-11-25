'''
Created on 21/11/2013

@author: johnefe
'''
import cv2
import numpy as np
import sys

im = cv2.imread('letras.png')
im3 = im.copy()
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
thresh2 = thresh.clip(1,0); 
#################      Now finding Contours         ###################
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
samples =  np.empty((0,1008))
responses = []
keys = [i for i in range(65,91)]

for cnt in contours:
    if cv2.contourArea(cnt)>50:
        [x,y,w,h] = cv2.boundingRect(cnt)
        if  h>34:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
            roi = thresh2[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(24,42))
            cv2.imshow('norm',im)
            key = cv2.waitKey(0)
            if key == 27:
                sys.exit()
            elif key in keys:
                #responses.append(int(chr(key)))
                responses.append(int(key))
                np.savetxt('letras/'+chr(key), roismall,fmt="%d")
                #10008 = 24*42
                sample = roismall.reshape((1,1008))
                samples = np.append(samples,sample,0)

responses = np.array(responses)
responses = responses.reshape((responses.size,1))
print ("Entrenamiento completo")

np.savetxt('letrasamples.data',samples,fmt="%d")
np.savetxt('letrasresponses.data',responses,fmt="%d")