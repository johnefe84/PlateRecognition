'''
Created on 10/10/2013
pyuic4 Ventana.ui -o Ventana.py
@author: johnefe
'''
import cv2

import Segmentacion
import Delimitacion
import Identificacion
import IdentificacionCorr
import sys
import numpy
import time
import cProfile, pstats
from io import StringIO
import ConexionBD
import Consulta_BD

#import threading

class Placas():
    resultados1=[]
    resultados2=[]
    
    def realizar_segmentacion(self,foto,ancho,alto,umbral,grosorvertical):
        self.resultados1=[]
        resultado, placaDetectada, colorDetectado, tiempoProcesamiento1=Segmentacion.Segmentar(foto,ancho,alto,umbral,grosorvertical)
        self.resultados1.append([resultado, placaDetectada, colorDetectado, tiempoProcesamiento1])
    
    def evaluarPlacaDetectada(self,placaDetectada,tiempoProcesamiento1,foto,tipoCamara,usuario,samplesl,responsesl,samplesn,responsesn,visitantesinregistro,pletras,pnumeros):
        identificado='??????'
        promedioGlobal='0.0'
        apagar='0'
        saludo_propietario=''
        resultadoDI=0
        minutos_pagar=0
        resultado=0
        procesadas=0
        mensaje=4
        tiempoProcesamiento2=0
        esdiplomatica=0
        rangos=[]
        
        rangos.append(7)
        rangos.append(5)
        rangos.append(11)

        try:
            for placaDetect in placaDetectada:
                if placaDetect != None:
                    #Realiza 3 intentos con diferentes configuraciones
                    for paso in range(1,4):
                        if paso==1:
                            #utiliza un metodo de binarizacion haciendo un poco borrosa la imagen para eliminar
                            #ruido
                            #genera caracteres mas delgados
                            placaDetect = cv2.GaussianBlur(placaDetect, (11, 11),0)
                            placaDetectBinaria=Segmentacion.binarizar(placaDetect,15)
                            placaDetectBinaria=Segmentacion.imfill(placaDetectBinaria,float(0.2))
                        elif paso==2:
                            #Utiliza un metodo sin quitar ruido con blur
                            #genera caracteres mas gruesos
                            placaDetect = Segmentacion.mejorarFoto(placaDetect)
                            placaDetectBinaria=cv2.inRange(placaDetect,80,255)
                            placaDetectBinaria=Segmentacion.imfill(placaDetectBinaria,float(0.1))
                        elif paso==3:
                            #toma una imagen invertida para encontrar placas diplomaticas
                            placaDetect = Segmentacion.mejorarFoto(placaDetect)
                            placaDetectBinaria=cv2.inRange(placaDetect,180,255)
                            placaDetectBinaria=Segmentacion.imfill(placaDetectBinaria,float(0.1))
                            placaDetectBinaria=placaDetectBinaria.clip(255,0)
                            
                        resultadoD, caracteres, tiempoProcesamiento2,cantidadAciertos,esmotoantigua,esdiplomatica=Delimitacion.Delimitar(placaDetectBinaria) 
                       
                        if resultadoD ==1:
                            #cv2.imshow('placa binaria',placaDetectBinaria)
                            #cv2.waitKey(1)
                            #realiza 2 intentos de identificacion diferentes
                            #primero utiliza los datos de delimitacion suponiendo que es moto antigua
                            #o suponiendo que es diplomatica
                            for paso2 in range(1,3):
                                resultadoDI,identificado,tiempoProcesamiento3,promedioGlobal=Identificacion.Identificar(caracteres,samplesl,responsesl,samplesn,responsesn,esmotoantigua,esdiplomatica,pletras,pnumeros) 
                                if resultadoDI==1: 
                                    tiempo=tiempoProcesamiento1+tiempoProcesamiento2+tiempoProcesamiento3
                                    resultado=1
                                    accion=''
                                    if tipoCamara == 'entrada':
                                        accion='insertar'                       
                                    elif tipoCamara=='salida':
                                        accion='retirar'
                                    else:    
                                        mensaje=3
                                        resultado=0
                                    if mensaje != 3:
                                        resultado,apagar,mensaje,saludo_propietario,minutos_pagar=self.insertarBaseDatos(identificado,accion,usuario,foto,visitantesinregistro)
#Super importante, si agrego mas opciones en los 2 for, debo cambiar estos dos valores para que salga del for
                                        paso=3
                                        paso2=4
                                        break
                                        
                                elif resultadoDI==0:
                                    #en el segundo intento omite lo que dijo la funcion delimitacion y fuerza a 
                                    #la validacion de placa particular o publica
                                    esmotoantigua=0
                                    esdiplomatica=0          
        except Exception as e:
            #print str(e)
            pass
        procesadas=procesadas+1
        if resultadoDI==1:
            procesadas=len(placaDetect)-1
        tiempo=tiempoProcesamiento1+tiempoProcesamiento2
        
        return identificado,tiempo,promedioGlobal,apagar,mensaje,resultadoDI,saludo_propietario,minutos_pagar
    
    def ProcesarImagen(self,foto,ancho,alto,tipoCamara,usuario,samplesl,responsesl,samplesn,responsesn,visitantesinregistro,pletras,pnumeros):
        #foto=cv2.resize(foto,(320,240))
        #ancho=foto.240
        #alto=320
        tam=foto.shape
        ancho=tam[0]
        alto=tam[1]
        threads2 = list()
        tic = time.time()
        caracteres_detectados='??????'
        promedioGlobal='0.0'
        apagar='0'
        saludo_propietario=''
        placaDetectada=foto
        tiempo_total=0
        grosorvertical=8
        resultado = 0
        minutos_pagar=0
        
        #Ingresa 2 veces, la primera con un grosorvertical=8 y el segundo=16
        for paso in range(1,3):
            resultado, placaDetectada, colorDetectado, tiempoProcesamiento1=Segmentacion.Segmentar(foto,ancho,alto)
            if resultado == 1:
                print ("placa detectada")
                caracteres_detectados,tiempo,promedioGlobal,apagar,mensaje,resultado,saludo_propietario,minutos_pagar=self.evaluarPlacaDetectada(placaDetectada,tiempoProcesamiento1,foto,tipoCamara,usuario,samplesl,responsesl,samplesn,responsesn,visitantesinregistro,pletras,pnumeros)
                tiempo4=time.time() - tic;
                #paso=3 para salir del for 
                break
            elif resultado==0:
                print ("placa no detectada")
                grosorvertical=grosorvertical*2
                mensaje= 2
                caracteres_detectados='??????'
                
        toc=time.time()
        tiempo_total=toc-tic
        #print 'tiempo_total '+str(tiempo_total)+ ' tiempo patron '+str(tiempoProcesamiento1)
        return resultado,tiempo_total,caracteres_detectados,promedioGlobal,mensaje,apagar,placaDetectada,saludo_propietario,minutos_pagar
    
    def insertarBaseDatos(self,placa,accion,usuario,foto,visitantesinregistro): 
        id_usuario=str(usuario[0])+str(usuario[1]);
        
        es_visitante=0
        autorizado=0
        out=''  
        resultado=0   
        mensaje=-1
        insertar=0
        huella_detectada=0
        saludo_propietario=''
        minutos_pagar=0
        validar_huella=0
        
        if visitantesinregistro==0:
            consulta = 'SELECT placa FROM vehiculos WHERE placa="' + placa + '";'
            valor, count_consulta1, resultado1=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'',str(id_usuario),'')
        
        if accion=='insertar':
            
            if visitantesinregistro==0:
                if valor == 1 and count_consulta1>0:
                    id_vehiculo=resultado1.fetchone()[0]
                    #determinar a quien o quienes pertenece el vehiculo registrado
                    consulta = 'SELECT id_propietarios FROM propietarios_vehiculos WHERE id_vehiculos="' + id_vehiculo +'";'
                    valor, count_consulta2, resultado2=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                    if valor == 1 and count_consulta2 >0:
                        for l in range(count_consulta2):
                            id_propietario=resultado2.fetchone()[0]
                            
                            #Se valida segun parametrizacion si se debe validar si el propietario se identifico con huella 
                            consulta = 'SELECT validar_huella,validar_tarjeta,nombres_propietario FROM propietarios where cedula="'+str(id_propietario)+'";'
                            valor5, count_consulta5, resultado5=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                            if valor5 == 1 and count_consulta5 >0:
                                validar_huella,validar_tarjeta,nombres_propietario = resultado5.fetchone()
                                #validar_huella=resultado5.fetchone()[0]
                                if validar_huella == 1 or validar_tarjeta == 1:
                                    #Se valida si en un rango de 5 minutos el conductor se identifico con la huella
                                    consulta = 'SELECT COUNT(*) FROM huellas_detectadas WHERE cedula =  "'+str(id_propietario)+'" AND fecha_entrada = CURDATE( ) AND MINUTE( TIMEDIFF( CURTIME( ) , hora_entrada ) ) <=5 and HOUR( TIMEDIFF( CURTIME( ) , hora_entrada ) ) =0 ;'
                                    valor4, count_consulta4, resultado4=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                                    if valor4 == 1 and count_consulta4 >0:
                                        huella_encontrada=resultado4.fetchone()[0]
                                        if huella_encontrada >= 1:
                                            huella_detectada=1
                                            saludo_propietario='Hola '+str(nombres_propietario)
                                        else:
                                            huella_detectada=0    
                                    else:
                                        huella_detectada=1                  
                                else:
                                    saludo_propietario='Hola '+str(nombres_propietario)
                                    huella_detectada=1     
                            else:
                                saludo_propietario='Hola '+str(nombres_propietario)
                                huella_detectada=1                                        
                                
                            #tomar los datos del propietario asi como si debe
                            #administracion o si no esta autorizado el ingreso
                            
                            consulta = 'SELECT nombres_propietario,apellidos_propietario,es_visitante,tiene_cartera,esta_autorizado FROM propietarios WHERE cedula=' +str(id_propietario) + ';'
                            valor, count_consulta3, resultado3=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                            if valor ==1 and count_consulta3 >0:
                                for k in range(count_consulta3):
                                    nombres_propietario, apellidos_propietario,es_visitante,tiene_cartera,esta_autorizado = resultado3.fetchone()
                                    if nombres_propietario != None:
                                        if es_visitante == 1:
                                            if esta_autorizado == 1: #si esta autorizado
                                                autorizado=autorizado+1
                                                resultado=1
                                            else:#si por algun motivo no esta autorizado a ingresar
                                                mensaje=7
                                        elif es_visitante == 0: #si es propietario
                                            if tiene_cartera == 1: #si debe administracion
                                                if esta_autorizado == 1: #si esta autorizado
                                                    autorizado=autorizado+1
                                                    resultado=1
                                                elif esta_autorizado == 0: #si por algun motivo no esta autorizado a ingresar
                                                    mensaje=8
                                            elif tiene_cartera == 0: #si no debe administracion
                                                if esta_autorizado == 1: #si esta autorizado
                                                    autorizado=autorizado+1
                                                    resultado=1
                                                elif esta_autorizado == 0: #si por algun motivo no esta autorizado a ingresar
                                                    mensaje=9
                                        #Hasta aqui el vehiculo es candidato para insertar en la tabla servicio_parqueo, pero debemos asegurarnos que no sea un vehiculo
                                        #que acaba de salir y que por error lo tomo la camara de entrada.
                                        consulta = 'SELECT count(*) FROM servicio_parqueo WHERE vehiculo="' +id_vehiculo + '" and fecha_salida= CURDATE( ) and MINUTE( TIMEDIFF( CURTIME( ) , hora_salida ) ) <=1;'
                                        valor4, count_consulta4, resultado4=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                                        if valor4 ==1 and count_consulta4 >0:
                                            ya_salio=resultado4.fetchone()[0]
                                            if (ya_salio>=1):
                                                autorizado=0
                                                mensaje=25 
                                    else:
                                        mensaje=10
                            else:
                                mensaje=11
                    else:    
                        mensaje=12   
                        resultado=0        
                else:
                    mensaje=13        
            elif visitantesinregistro==1:
                #Esta seccion funciona como ideautopublico
                huella_detectada=1
                saludo_propietario='Hola'
                id_vehiculo=resultado1.fetchone()[0]
                   
                consulta = 'select propietarios from cupos_disponibles;'
                valor, count_consulta4, resultado4=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                if valor ==1 :
                    cupos_propietarios=resultado4.fetchone()[0]
        
                    if cupos_propietarios > 0:
                        insertar=1
                    else:
                        mensaje=15                 
                          
                if insertar==1:
                    consulta = 'SELECT count(*) FROM servicio_parqueo WHERE vehiculo="' +id_vehiculo + '" and fecha_salida= CURDATE( ) and MINUTE( TIMEDIFF( CURTIME( ) , hora_salida ) ) <=5;'
                    valor4, count_consulta4, resultado4=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                    if valor4 ==1 and count_consulta4 >0:
                        ya_salio=resultado4.fetchone()[0]
                        if (ya_salio>=1):
                            autorizado=0
                            mensaje=25 
                        else:
                            valor, count_consulta, out=Consulta_BD.realizar_consulta_base_datos('insertarVehiculo',placa,'99999999','','',id_usuario,foto)
                            if valor == 1: 
                                resultado=1
                                mensaje=5
                            else:
                                mensaje=16 
      
            if visitantesinregistro==0:
                if autorizado >0:
                    if huella_detectada==1:
                        consulta = 'select propietarios,visitantes from cupos_disponibles;'
                        valor, count_consulta4, resultado4=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                        if valor ==1 :
                            cupos_propietarios,cupos_visitantes=resultado4.fetchone()
                            if es_visitante==1:
                                if cupos_visitantes > 0:
                                    insertar=1
                                else:
                                    mensaje=14 
                            else:
                                if cupos_propietarios > 0:
                                    insertar=1
                                else:
                                    mensaje=15    
                        if insertar==1:
                            consulta = 'SELECT count(*) FROM servicio_parqueo WHERE vehiculo="' +id_vehiculo + '" and fecha_salida= CURDATE( ) and MINUTE( TIMEDIFF( CURTIME( ) , hora_salida ) ) <=1;'
                            valor4, count_consulta4, resultado4=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                            if valor4 ==1 and count_consulta4 >0:
                                ya_salio=resultado4.fetchone()[0]
                                if (ya_salio>=1):
                                    autorizado=0
                                    mensaje=25 
                                else:
                                    valor, count_consulta, out=Consulta_BD.realizar_consulta_base_datos('insertarVehiculo',id_vehiculo,id_propietario,'','',id_usuario,foto)
                                    if valor == 1: 
                                        resultado=1
                                        mensaje=5
                                    else:
                                        mensaje=16 
                                        resultado=0
                    else:
                        mensaje=22 
                        resultado=0            
                else:
                    if validar_huella==1 and huella_detectada==0: 
                        mensaje=22 
                        resultado=0
                        out=''
                    else:
                        if mensaje != 25:
                            mensaje=17 
                            resultado=0
                            out=''
                        else:
                            resultado=0
                            out=''
                
        if accion=='retirar':
            if visitantesinregistro==0:
                if valor == 1 and count_consulta1>0:
                    id_vehiculo=resultado1.fetchone()[0]
                    consulta = 'SELECT id_propietarios FROM propietarios_vehiculos WHERE id_vehiculos="'+id_vehiculo+'";'
                    valor, count_consulta2, resultado5=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                    if valor == 1 and count_consulta2 >0:
                        for l in  range(count_consulta2):
                            id_propietario=str(resultado5.fetchone()[0])
                            consulta = 'SELECT valor_minuto FROM parqueadero;'
                            valor6, count_consulta6, resultado6=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                            if valor6 == 1 and count_consulta6 >0:
                                valor_minuto=resultado6.fetchone()[0]
                                #Se valida segun parametrizacion si se debe validar si el propietario se identifico con huella 
                            consulta = 'SELECT validar_huella,validar_tarjeta,nombres_propietario FROM propietarios where cedula="'+str(id_propietario)+'";'
                            valor5, count_consulta5, resultado5=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                            if valor5 == 1 and count_consulta5 >0:
                                validar_huella,validar_tarjeta,nombres_propietario = resultado5.fetchone()                    
                                if validar_huella == 1 or validar_tarjeta == 1:
                                    #Se valida si en un rango de 5 minutos el conductor se identifico con la huella
                                    consulta = 'SELECT COUNT(*) FROM huellas_detectadas WHERE cedula =  "'+str(id_propietario)+'" AND fecha_entrada = CURDATE( ) AND MINUTE( TIMEDIFF( CURTIME( ) , hora_entrada ) ) <=5 and HOUR( TIMEDIFF( CURTIME( ) , hora_entrada ) ) =0 ;'
                                    valor4, count_consulta4, resultado4=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                                    if valor4 == 1 and count_consulta4 >0:
                                        huella_encontrada=resultado4.fetchone()[0]
                                        if huella_encontrada >= 1:
                                            huella_detectada=1
                                            mensaje=6 
                                            saludo_propietario='Adios '+str(nombres_propietario)
                                        else:
                                            mensaje=22
                                            huella_detectada=0                                      
                                    else:
                                        huella_detectada=1        
                                else:
                                    mensaje=6 
                                    saludo_propietario='Adios '+str(nombres_propietario)
                                    huella_detectada=1     
                            else:
                                saludo_propietario='Adios '+str(nombres_propietario)
                                huella_detectada=1                                        
                                
                            #tomar los datos del propietario asi como si debe
                            #administracion o si no esta autorizado el ingreso
                            if huella_detectada==1:
                                consulta = 'SELECT nombres_propietario,apellidos_propietario,es_visitante,tiene_cartera,esta_autorizado FROM propietarios WHERE cedula="' +str(id_propietario) + '";'
                                valor, count_consulta3, resultado3=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                                if valor ==1 and count_consulta3 >0:
                                    for k in range(count_consulta3):
                                        nombres_propietario, apellidos_propietario,es_visitante,tiene_cartera,esta_autorizado = resultado3.fetchone()
                                        
                                valor, minutos_pagar, out=Consulta_BD.realizar_consulta_base_datos('retirarVehiculo',id_vehiculo,id_propietario,'',valor_minuto,str(id_usuario),'');
                                if valor ==1 : 
                                    if es_visitante == 1: 
                                        if esta_autorizado == 0:
                                            mensaje=18
                                        else:
                                            mensaje=6 
                                    else:
                                        mensaje=6    
                                        out=''
                                    resultado=1
                                else:
                                    mensaje=19
                                    out=''  
                                    resultado=0
                            else:
                                if huella_encontrada == 0:
                                    mensaje=22        
                                else:    
                                    mensaje=23
                    else:
                        out=''  
                        resultado=0
                        mensaje=20
                else:    
                    out=''  
                    resultado=0   
                    mensaje=21 
            elif visitantesinregistro==1: 
                consulta = 'SELECT valor_minuto FROM parqueadero;'
                valor6, count_consulta6, resultado6=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                if valor6 == 1 and count_consulta6 >0:
                    valor_minuto=resultado6.fetchone()[0]     
                    mensaje=6 
                    saludo_propietario='Adios '
                    valor, minutos_pagar, out=Consulta_BD.realizar_consulta_base_datos('retirarVehiculo',placa,'99999999','',valor_minuto,str(id_usuario),'');
                    if valor ==1 : 
                        mensaje=6   
                        resultado=1
                    else:
                        mensaje=19
                        out=''  
                        resultado=0               
                else:
                    saludo_propietario='Adios '   
                                   
        return resultado,out,mensaje,saludo_propietario, minutos_pagar
