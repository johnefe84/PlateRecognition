import Placas
import cv2
import numpy as np

samplesl = np.loadtxt('./letrasamples.data',np.float32)
responsesl = np.loadtxt('./letrasresponses.data',np.float32)
samplesn = np.loadtxt('./numerosamples.data',np.float32)
responsesn = np.loadtxt('./numerosresponses.data',np.float32)
im = cv2.imread('/Users/johnefe/Documents/placas-dia/placa1.jpg')
out = np.zeros(im.shape,np.uint8)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
height,width= gray.shape
placas=Placas.Placas()
pletras = None
pnumeros = None
tipoCamara = "IP"
usuario = "usuario"
visitantesinregistro = 0

resultado,tiempo_total,caracteres_detectados,promedioGlobal,mensajes,apagar,placaDetectada,saludo_propietario,minutos_pagar=placas.ProcesarImagen(gray,height,width,tipoCamara,usuario,samplesl,responsesl,samplesn,responsesn,visitantesinregistro,pletras,pnumeros)