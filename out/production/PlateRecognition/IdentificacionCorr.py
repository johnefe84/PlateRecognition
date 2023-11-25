'''
Created on 5/01/2014

@author: johnefe
'''
import Correlacion
import numpy as np
import time

def Identificar(caracteres):
    tic = time.time()
    exito=3;
    tiempoProcesamiento=0;
    resultado=[];
    samplesl = np.loadtxt('letras.data',np.float32)
    samplesl2 = np.loadtxt('letrasamples.data',np.float32)
    
    samplesn = np.loadtxt('numeros.data',np.float32)
    letras= samplesl.reshape((24,42))
    numeros= samplesn.reshape((24,42))
    porcentaje1=[];
    porcentaje2=[];
    alfab=['A','B','C','D','E','F','G','H','I','J','K','L','M',
                      'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];
    digits=['1','2','3','4','5','6','7','8','9','0'];
    alfabeto=np.array(alfab);
    digitos=np.array(digits);
    try:
        for contador in range(0,6):
            if contador in range(0,3):
                for letra in letras:
                    porcentaje1.append(Correlacion.corr2(caracteres[contador],letra))
                maximo=max(porcentaje1)  
                if maximo > 0.7:
                    #string = chr(int((resultsl[0][0])))
                    string=list(alfabeto).index(maximo);
                    resultado.append(string)
                    exito=1
            else:   
                for numero in numeros: 
                    porcentaje2.append(Correlacion.corr2(caracteres[contador],numero))
                maximo2=max(porcentaje2)  
                if maximo2 > 0.7:
                    #string = chr(int((resultsl[0][0])))
                    string2=list(digitos).index(maximo2);
                    resultado.append(string2)
                    exito=1
                #string = chr(int((resultsn[0][0]))) 
                #resultado.append(string)
                #exito=1
    except Exception as e:
        exito=0;
        resultado='??????';            
          
    tiempoProcesamiento3=time.time() - tic;  
    #print('tiempo en segundos de Identificacion:'+str(tiempoProcesamiento3))
    return exito,''.join(resultado),tiempoProcesamiento