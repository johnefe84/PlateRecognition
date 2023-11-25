'''
Created on 24/10/2013

@author: johnefe
'''
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
import cv2
import Segmentacion
import placas
import Image
import numpy as np
import pdf417
import time

CV_CAP_PROP_POS_MSEC=0# Current position of the video file in milliseconds.
CV_CAP_PROP_POS_FRAMES=1# 0-based index of the frame to be decoded/captured next.
CV_CAP_PROP_POS_AVI_RATIO=2# Relative position of the video file: 0 - start of the film, 1 - end of the film.
CV_CAP_PROP_FRAME_WIDTH=3# Width of the frames in the video stream.
CV_CAP_PROP_FRAME_HEIGHT=4# Height of the frames in the video stream.
CV_CAP_PROP_FPS=5# Frame rate.
CV_CAP_PROP_FOURCC=6# 4-character code of codec.
CV_CAP_PROP_FRAME_COUNT=7# Number of frames in the video file.
CV_CAP_PROP_FORMAT=8# Format of the Mat objects returned by retrieve() .
CV_CAP_PROP_MODE=9# Backend-specific value indicating the current capture mode.
CV_CAP_PROP_BRIGHTNESS=10# Brightness of the image (only for cameras).
CV_CAP_PROP_CONTRAST=11# Contrast of the image (only for cameras).
CV_CAP_PROP_SATURATION=12# Saturation of the image (only for cameras).
CV_CAP_PROP_HUE=13# Hue of the image (only for cameras).
CV_CAP_PROP_GAIN=14# Gain of the image (only for cameras).
CV_CAP_PROP_EXPOSURE=15# Exposure (only for cameras).
CV_CAP_PROP_CONVERT_RGB=16# Boolean flags indicating whether images should be converted to RGB.
CV_CAP_PROP_WHITE_BALANCE=17# Currently unsupported
CV_CAP_PROP_RECTIFICATION=18# Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend 

class ColourTracker:
    def __init__(self):
        #cv2.namedWindow("ColourTrackerWindow",320)
        #self.capture=cv2.VideoCapture('parqueadero_paez.avi')
        #self.capture=cv2.VideoCapture('I:\worlspace\parqueadero_paez.avi')
        #self.capture=cv2.imread('I:\worlspace\replacol\placas\letras.PNG')
        self.capture=cv2.VideoCapture(2)
            
        #self.capture.set(CV_CAP_PROP_BRIGHTNESS,0)
        #self.capture.set(CV_CAP_PROP_CONTRAST,100)
        #self.capture.set(CV_CAP_PROP_WHITE_BALANCE,1)
        #self.capture.set(CV_CAP_PROP_GAIN,0)
        #self.capture.set(CV_CAP_PROP_HUE,0)
        
        cv2.namedWindow("Prueba de reconocimiento", cv2.CV_WINDOW_AUTOSIZE)
        #cv2.namedWindow("Prueba de reconocimiento2", cv2.CV_WINDOW_AUTOSIZE)
                
        #propiedades=self.capture.get(cv.cv)
        self.scale_down = 4

    def run(self):
        contador=0
        samplesl = np.loadtxt('letrasamples.data',np.float32)
        responsesl = np.loadtxt('letrasresponses.data',np.float32)
        samplesn = np.loadtxt('numerosamples.data',np.float32)
        responsesn = np.loadtxt('numerosresponses.data',np.float32)
        while True:# and contador <=30:
            f, orig_img = self.capture.read()
            #orig_img=cv2.imread('numeros.PNG')
            #orig_img =Image.open("plate14.jpg")
            if orig_img != None:
                orig_img =cv2.cvtColor(orig_img,cv2.COLOR_BGR2GRAY)
                tam=orig_img.shape
                ancho=tam[0]
                alto=tam[1]
                #kernel = np.ones((5,5),np.uint8)
                #orig_img2= cv2.dilate(orig_img,kernel,iterations = 3)
                #orig_img= cv2.erode(orig_img,kernel,iterations = 0)
                #orig_img=orig_img+0.5
                #orig_img =cv2.cvtColor(orig_img,cv2.COLOR_RGB2HSV)
                
                #caracteres_detectados,promedioGlobal,mensaje,apagar,orig_img2,nombres=placas.ProcesarImagen(orig_img, ancho, alto,'entrada','10|Vigilante de turno',samplesl,responsesl,samplesn,responsesn)
                #if caracteres_detectados <> '??????': 
                #    print('caracteres_detectados: '+ caracteres_detectados)
                #resultado, orig_img2, orig_img3, tiempoProcesamiento1 = Segmentacion.Segmentar(orig_img,ancho,alto)
                #orig_img2=Segmentacion.detectarReflectivo(orig_img2) 
                #cv2.drawContours(orig_img,[box],0,(0,0,255),2)
                #valor=pdf417.pdf417_decode(orig_img)
                #print(valor)
                #cv2.circle(orig_img,(punto1y,punto1x),2,[0,0,255],-1)
                #cv2.circle(orig_img,(punto2y,punto2x),2,[0,0,255],-1)
                #cv2.circle(orig_img,(punto3y,punto3x),2,[0,0,255],-1)
                #cv2.circle(orig_img,(punto4y,punto4x),2,[0,0,255],-1)
                # create a CLAHE object (Arguments are optional).
                #cv2.equalizeHist( orig_img, orig_img );
                #orig_img3=Segmentacion.mejorarFoto(orig_img2,ancho,alto)
                #orig_img3=Segmentacion.binarizar(orig_img3)
                #orig_img2=Segmentacion.mejorarFoto(orig_img2,ancho,alto)
                #orig_img2=Segmentacion.detectarReflectivo(orig_img2) 
                #cv2.imshow("Prueba de reconocimiento2",orig_img2  )
                #cv2.waitKey(10)
            
                cv2.imshow("Prueba de reconocimiento", orig_img)
                cv2.waitKey(10)
                #print(contador)
                contador=contador+1
            
#if __name__ == "__main__":
'''
for contador in range(0,2):
    capture=cv2.VideoCapture(contador)
    orig_img = capture.retrieve()
    if orig_img <> None:
        print ('la camara ' + str(contador+1) + ' esta conectada')
 '''   
colour_tracker = ColourTracker()
colour_tracker.run()