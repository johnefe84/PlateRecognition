import Placas
import cv2
import numpy as np
import os
import sys


samplesl = np.loadtxt(os.path.join(sys.path[0], "templates/letrasamples.data"), np.float32)
responsesl = np.loadtxt(os.path.join(sys.path[0], "templates/letrasresponses.data"),np.float32)
samplesn = np.loadtxt(os.path.join(sys.path[0], "templates/numerosamples.data"),np.float32)
responsesn = np.loadtxt(os.path.join(sys.path[0], "templates/numerosresponses.data"),np.float32)
FotoOriginal = cv2.imread('/Users/john.ruiz/placa3.jpg')
out = np.zeros(FotoOriginal.shape,np.uint8)
gray = cv2.cvtColor(FotoOriginal,cv2.COLOR_BGR2GRAY)
height,width= gray.shape
placas=Placas.Placas()
pletras = None
pnumeros = None
tipoCamara = "IP"
usuario = "usuario"
visitantesinregistro = 0

resultado,tiempo_total,caracteres_detectados,promedioGlobal,mensajes,apagar,placaDetectada,saludo_propietario,minutos_pagar=placas.ProcesarImagen(gray,height,width,tipoCamara,usuario,samplesl,responsesl,samplesn,responsesn,visitantesinregistro,pletras,pnumeros, FotoOriginal)
