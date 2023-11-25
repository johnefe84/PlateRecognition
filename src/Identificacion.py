'''
Created on 10/10/2013

@author: johnefe
'''
import time
import numpy as np
import cv2
import Correlacion
PORCENTAJE_ACIERTO=0.48


def Identificar(caracteres,samplesl,responsesl,samplesn,responsesn):
    #Computa la correlacion entre la plantilla y la imagen de entrada
    tic = time.time()
    exito=3;
    cantidadAciertos=0;
    tiempoProcesamiento=0;
    resultado=[];
    promedioGlobal=0;
    
    #######   training part    ###############
    #samplesl = np.loadtxt('letrasamples.data',np.float32)
    #responsesl = np.loadtxt('letrasresponses.data',np.float32)
    #samplesn = np.loadtxt('numerosamples.data',np.float32)
    #responsesn = np.loadtxt('numerosresponses.data',np.float32)

    responsesn = responsesn.reshape((responsesn.size,1))
    modeln = cv2.KNearest()
    modeln.train(samplesn,responsesn)

    responsesl = responsesl.reshape((responsesl.size,1))
    modell = cv2.KNearest()
    modell.train(samplesl,responsesl)
    
    #Guardar datos de entrenamiento para cargarlos mas tarde
    #with open('objetosOCR.pickle', 'w') as file:
    #    pickle.dump([modell, modeln], file,pickle.HIGHEST_PROTOCOL)
        
    try:
        for contador in range(0,6):
            #np.savetxt("roismall.csv",  caracteres[contador], delimiter=",",fmt="%d") 
            roismall = caracteres[contador].reshape((1,1008))
            roismall = np.float32(roismall)
            if contador in range(0,3):
                retvall, resultsl, neigh_respl, distsl = modell.find_nearest(roismall, k = 1)
                string = chr(int((resultsl[0][0])))
                
                letra = np.loadtxt('letras/'+string,np.float32)
                porcentaje=Correlacion.corr2(caracteres[contador],letra)
                 
                if porcentaje >= PORCENTAJE_ACIERTO :
                    resultado.append(string)
                    cantidadAciertos=cantidadAciertos+1
                else:
                    letra2 = np.loadtxt('letras/'+string+'2',np.float32)
                    porcentaje2=Correlacion.corr2(caracteres[contador],letra2)
                    
                    if porcentaje2 >= PORCENTAJE_ACIERTO :
                        resultado.append(string)
                        cantidadAciertos=cantidadAciertos+1
                        porcentaje=porcentaje2
                    else:    
                        porcentaje=0
                        resultado.append('?')  
                        
                promedioGlobal=promedioGlobal+porcentaje         
                #print("letra "+ str(porcentaje)+" , "+str(porcentaje2)) 
                #porcentaje=80    
                #promedioGlobal=promedioGlobal+porcentaje
                #resultado.append(string)
                #cantidadAciertos=cantidadAciertos+1
            else:    
                retvaln, resultsn, neigh_respn, distsn = modeln.find_nearest(roismall, k = 1)
                string = chr(int((resultsn[0][0]))) 
                
                numero = np.loadtxt('numeros/'+string,np.float32)
                porcentaje=Correlacion.corr2(caracteres[contador],numero)      
                                    
                if porcentaje >= PORCENTAJE_ACIERTO :
                    resultado.append(string)
                    cantidadAciertos=cantidadAciertos+1
                else:
                    numero2 = np.loadtxt('numeros/'+string+'2',np.float32)
                    porcentaje2=Correlacion.corr2(caracteres[contador],numero2)
                    
                    if porcentaje2 >= PORCENTAJE_ACIERTO :
                        resultado.append(string)
                        cantidadAciertos=cantidadAciertos+1
                        porcentaje = porcentaje2 
                    else: 
                        porcentaje=0
                        resultado.append('?')   
                promedioGlobal=promedioGlobal+porcentaje         
                #print("numero "+ str(porcentaje)+" , "+str(porcentaje2)) 
                #porcentaje=80    
                #promedioGlobal=promedioGlobal+porcentaje
                #resultado.append(string)
                #cantidadAciertos=cantidadAciertos+1       
                    
    except Exception as e:
        resultado='??????';            
          
    tiempoProcesamiento=time.time() - tic;  
    promedioGlobal=(round((promedioGlobal/6) , 2))*100; 
       
    if cantidadAciertos == 6 and promedioGlobal >=PORCENTAJE_ACIERTO:
        exito=1
        print ("Identificado: " + ''.join(resultado)+' tiempo: '+str(tiempoProcesamiento)+' segs.')+" "+str(promedioGlobal)+"%"; 
    else:
        'Se pone todo en signo ? para evitar cosas como JFR4?5'
        resultado='??????'
        print ("Identificado parcial: " + ''.join(resultado)+' promedioGlobal: '+str(promedioGlobal)); 
        exito=0             
       
    #print('tiempo en segundos de Identificacion:'+str(tiempoProcesamiento3))
    return exito,''.join(resultado),tiempoProcesamiento,promedioGlobal