'''
Created on 8/10/2013

@author: johnefe
'''
import time
import numpy as np
import Patron
import cv2

MOSTRAR_IMAGEN_BINARIA = True

def binarizar(imagen_gris):
    #imagen_binaria = cv2.adaptiveThreshold(imagen_gris,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2) #esto generara muchisimos boundaries
    ret,imagen_binaria = cv2.threshold(imagen_gris,100,255,cv2.THRESH_OTSU)
    return imagen_binaria

def Segmentar(FOTO,ancho,alto,FotoOriginal):
    tic = time.time() 
    #colorDetectado= detectarReflectivo(FOTO)
    imagenBinaria = binarizar(FOTO)
    #FOTOriginal=colorDetectado;                
    kernel = np.ones((5,5),np.uint8)
    #imagenBinaria= cv2.dilate(imagenBinaria,kernel,iterations = 3)
    #imagenBinaria= cv2.erode(imagenBinaria,kernel,iterations = 3)
    print ("voy a buscar patron")
    if(MOSTRAR_IMAGEN_BINARIA):
        cv2.imshow('buscarPatron:imagenBinaria',imagenBinaria)
        cv2.waitKey(0)
    resultado, placaDetectada,tiempoProcesamiento1=Patron.buscarPatron(imagenBinaria,FOTO,ancho,alto,FotoOriginal);
    #placaDetectada=mejorarFoto(placaDetectada,ancho,alto)
    #placaDetectada=binarizar(placaDetectada)
    tiempoProcesamiento0=time.time() - tic; 
    return resultado, placaDetectada, imagenBinaria, tiempoProcesamiento0


def transformar(FOTO,ancho,alto,pts1,pts2):
    #Los puntos van de izquierda a derecha de arriba a bajo como una Z
    #pts1 = np.float32([[8,1],[145,20],[1,59],[135,75]])
    #pts2 = np.float32([[0,0],[145,0],[0,75],[145,75]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    FOTO_transformada = cv2.warpPerspective(FOTO,M,(alto,ancho))
    return FOTO_transformada 
       
def mejorarFoto(FOTO,ancho,alto):
    #FOTOHSV = cv2.cvtColor(FOTO,cv2.COLOR_RGB2HSV)
    HSVMEJORADA = np.zeros( (ancho,alto, 3), np.uint8)
    #H=FOTOHSV[:,:,0]
    #S=FOTOHSV[:,:,1]
    #V=FOTOHSV[:,:,2]
    #V2 = cv2.equalizeHist(V)
    #HSVMEJORADA[:,:,0]=H
    #HSVMEJORADA[:,:,1]=S
    #HSVMEJORADA[:,:,2]=V2
    #mejorar conctraste
    FOTO = cv2.equalizeHist(FOTO)
    #RGBMEJORADA = cv2.cvtColor(HSVMEJORADA,cv2.COLOR_HSV2RGB)
    #return HSVMEJORADA,RGBMEJORADA
    return FOTO

def detectarReflectivo(imagen_gris):
    colorDetectado=cv2.inRange(imagen_gris,165,255)
    #cv2.imshow('detectarReflectivo',colorDetectado)
    #cv2.waitKey(10) 
    return colorDetectado
    
def detectarAmarillo(RGBMEJORADA):
    C=255-RGBMEJORADA[:,:,0]
    M=255-RGBMEJORADA[:,:,1]
    Y=255-RGBMEJORADA[:,:,2]
    C2=cv2.inRange(C,110,255)
    M2=cv2.inRange(M,0,140)
    Y2=cv2.inRange(Y,0,120)
   
    amarilloDetectado=C2&M2&Y2
    return amarilloDetectado

def detectarBlanco(HSV):
    H=HSV[:,:,0]
    S=HSV[:,:,1]
    V=HSV[:,:,2]
    Hdetect=cv2.inRange(H,0,100)
    Sdetect=cv2.inRange(S,0,180) 
    Vdetect=cv2.inRange(V,180,255)
    blancoDetectado=Sdetect&Vdetect
    blancoDetectado=blancoDetectado.clip(0,1)
    return blancoDetectado
