'''
Created on 2/12/2013

@author: johnefe
'''
import cv2
import numpy as np
from PyQt5 import QtGui, QtCore, Qt
from Ventana import Ui_Ventana
import Placas
import urllib 
import Segmentacion
import XMLConfig
import time
import urllib
from io import StringIO
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import  io

class Video():
    #readFrame=None
    
    def __init__(self,captura):   
        self.capture=captura
        self.readFrame=np.array([])         
        self.currentFrame=np.array([])
 
    def test_video(self,tipo,direccion):
        exitoso=False
        if (tipo == 'CCTV'):
            time.sleep(2)
            exitoso, self.readFrame  = self.capture.read()
            #if exitoso:
            #    if sum(sum(sum(self.readFrame)))==0:
            #        exitoso=0
            #        print 'Sin fuente de video en camara: '+str(tipo)+' direccion: '+str(direccion)
        
        elif(tipo == 'IP'):  
            try:
                image = urllib.urlopen(direccion).read()
                image_as_file = io.BytesIO(image)
                image_as_pil = Image.open(image_as_file)
                draw = ImageDraw.Draw(image_as_pil)
                self.readFrame = np.array(image_as_pil)  
                exitoso=True   
            except:
                exitoso=False
                pass
            
        return exitoso    
    
    def capturar_imagen(self,direccion):
        orig_imagen=None
        try:
            image = urllib.urlopen(direccion).read()
            # convert directly to an Image instead of saving / reopening
            # thanks to SO: http://stackoverflow.com/a/12020860/377366
            image_as_file = io.BytesIO(image)
            image_as_pil = Image.open(image_as_file)
            draw = ImageDraw.Draw(image_as_pil)
            orig_imagen = np.array(image_as_pil)
        except:
            pass
        return orig_imagen
            
    def captureNextFrame(self,tipoCamara,usuario,tipo,direccion,samplesl,responsesl,samplesn,responsesn,visitantesinregistro,x1,x2,x3,x4,y1,y2,y3,y4,rot,redmx,redmy,umbral,pletras,pnumeros):
        """                                         
        capture frame and reverse RBG BGR and return opencv image                                                                        
        """       
        apagar='0'
        saludo_propietario=''
        caracteres_detectados=''
        promedioGlobal=0
        placaDetectada=None
        mensajes=0
        exitoso=False
        minutos_pagar=0
        tiempo_total=0

        if (tipo == 'CCTV'):
            exitoso, self.readFrame  = self.capture.read()
        elif(tipo == 'IP'):  
            seguir=False
            self.readFrame = self.capturar_imagen(direccion)
            if self.readFrame != None:
                exitoso=True
                seguir=True
            else:
                seguir=False
                exitoso=False
            
        if(exitoso == True):
            #self.currentFrame=self.readFrame
            try:
                self.currentFrame = cv2.cvtColor(self.readFrame,cv2.COLOR_BGR2GRAY)
                tam=self.currentFrame.shape
                #ancho=tam[0]
                #alto=tam[1]
                #self.currentFrame=cv2.resize(self.currentFrame,(720,480))
                height,width=self.currentFrame.shape
                try:
                    #x1,x2,x3,x4,y1,y2,y3,y4,redmx,redmy,umbral=XMLConfig.leer_datos_puntos(tipoCamara)
                    self.currentFrame=Segmentacion.rotarAngulo(self.currentFrame,height,width,x1,x2,x3,x4,y1,y2,y3,y4,rot,redmx,redmy)
                except Exception as error:
                    print("Error en archivo config.xml" +error)
                    exit()
                    
                placaDetectada=self.currentFrame
                placas=Placas.Placas()
                resultado,tiempo_total,caracteres_detectados,promedioGlobal,mensajes,apagar,placaDetectada,saludo_propietario,minutos_pagar=placas.ProcesarImagen(self.currentFrame,height,width,tipoCamara,usuario,samplesl,responsesl,samplesn,responsesn,visitantesinregistro,umbral,pletras,pnumeros)  
            except Exception as e:
                print("except: "+str(tipoCamara))
                mensajes=24  
                pass
        else:  
            print("Sin imagen en: "+str(tipoCamara))
            caracteres_detectados="??????"
            promedioGlobal=0
            mensajes=24            
        return caracteres_detectados,promedioGlobal,mensajes,apagar,placaDetectada,saludo_propietario,minutos_pagar,tiempo_total 
    
    def update(self,imagen,ancho,alto): 
        #tam=imagen.shape
        #ancho=tam[0]
        #alto=tam[1]
        x1 = cv2.getTrackbarPos('x1', 'original')
        x2 = cv2.getTrackbarPos('x2', 'original')
        x3 = cv2.getTrackbarPos('x3', 'original')
        x4 = cv2.getTrackbarPos('x4', 'original')
        y1 = cv2.getTrackbarPos('y1', 'original')
        y2 = cv2.getTrackbarPos('y2', 'original')
        y3 = cv2.getTrackbarPos('y3', 'original')
        y4 = cv2.getTrackbarPos('y4', 'original')
        rot = cv2.getTrackbarPos('rot', 'original')
        redmx = cv2.getTrackbarPos('redimensionX', 'original')
        redmy = cv2.getTrackbarPos('redimensionY', 'original')
        
        imagen=Segmentacion.rotarAngulo(imagen,ancho,alto,x1,x2,x3,x4,y1,y2,y3,y4,rot,redmx,redmy)
        #dim = (320,240)
        #imagen2=cv2.resize(imagen,dim,cv2.INTER_AREA)
        #cv2.imshow("original", imagen)
        #cv2.waitKey(0)
        return imagen
    
    def mostrarFrame(self,imagen):
        try:
            height,width=imagen.shape[:2]
            img=QtGui.QImage(imagen,
                              width,
                              height,
                              QtGui.QImage.Format_Indexed8)
            img=QtGui.QPixmap.fromImage(img)
            return img
        except:
            return None        
            
    def convertFrame(self):
        """converts frame to format suitable for QtGui            """
        try:
            #self.readFrame=cv2.cvtColor(self.readFrame, cv2.cv.CV_BGR2RGB, self.readFrame)
            #self.currentFrame
            height,width=self.currentFrame.shape[:2]
            img=QtGui.QImage(self.currentFrame,
                              width,
                              height,
                              QtGui.QImage.Format_Indexed8)
            #Format_RGB888
            img=QtGui.QPixmap.fromImage(img)
            # .Format_Indexed8
            return img
        except:
            return None
        