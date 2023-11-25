'''
Created on 23/11/2013

@author: johnefe
'''
import cv2
import numpy as np

#######   training part    ###############
samplesl = np.loadtxt('letrasamples.data',np.float32)
responsesl = np.loadtxt('letrasresponses.data',np.float32)
samplesn = np.loadtxt('numerosamples.data',np.float32)
responsesn = np.loadtxt('numerosresponses.data',np.float32)

responsesn = responsesn.reshape((responsesn.size,1))
modeln = cv2.ml.KNearest_create()
modeln.train(samplesn, cv2.ml.ROW_SAMPLE, responsesn)

responsesl = responsesl.reshape((responsesl.size,1))
modell = cv2.ml.KNearest_create()
modell.train(samplesl, cv2.ml.ROW_SAMPLE, responsesl)
############################# testing part  #########################
im = cv2.imread('/Users/johnefe/Documents/placas-dia/placa1.jpg')
out = np.zeros(im.shape,np.uint8)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
thresh2 = thresh.clip(0,1); 
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt)>50:
        [x,y,w,h] = cv2.boundingRect(cnt)
        if  h>39:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
            roi = thresh2[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(24,42))
            np.savetxt("b.csv",  roismall, delimiter=",",fmt="%d") 
            roismall = roismall.reshape((1,1008))
            roismall = np.float32(roismall)
            retvall, resultsl, neigh_respl, distsl = modell.findNearest(roismall, k = 1)
            retvaln, resultsn, neigh_respn, distsn = modeln.findNearest(roismall, k = 1)
            if distsl < distsn:
                string = chr(int((resultsl[0][0])))
            else:
                string = chr(int((resultsn[0][0])))    
            cv2.putText(out,string,(x,y+h),0,1,(0,255,0))
cv2.imshow('im',im)
cv2.imshow('out',out)
cv2.waitKey(0)