'''
Created on 10/10/2013

@author: johnefe
'''
import time
import numpy
import cv2
import scipy.misc

def bwtraceboundary(PLACA,posicionInicialY,posicionInicialX,cordenadaY,cordenadaX,cantidadCoord):
    Boundaries = []
    x=posicionInicialX;
    y=posicionInicialY;
    Boundaries.append([y,x]);
    minX=cordenadaX;
    minY=cordenadaY;
    maxX=0;
    maxY=0;
    callejonArriba=0;
    callejonAbajo=0;
    callejonIzquierdo=0;
    callejonDerecho=0;

    try:
        for contador in range(1,cantidadCoord):                 
            #Se analiza el valor de los 8 vecinos del pixel similar al telcado numerico
            #en orden contrario a las manecillas del relog
            if x >0 and y < cordenadaY:
                veci1=PLACA[y+1,x-1]; 
            else:
                veci1=1;         
            
            if y < cordenadaY:    
                veci2=PLACA[y+1,x];
            else:
                veci2=1;          
               
            if x < cordenadaX and y < cordenadaY:    
                veci3=PLACA[y+1,x+1];
            else:
                veci3=1;      
                
            if x < cordenadaX:    
                veci6=PLACA[y,x+1];  
            else:
                veci6=1;    
                
            if x < cordenadaX and y > 0:    
                veci9=PLACA[y-1,x+1];
            else:
                veci9=1;     
                  
            if y > 0:      
                veci8=PLACA[y-1,x];
            else:
                veci8=1;      
                 
            if x > 0 and y > 0: 
                veci7=PLACA[y-1,x-1];
            else:
                veci7=1;       
                 
            if x > 0:    
                veci4=PLACA[y,x-1];
            else:
                veci4=1;     
   
            #El programa inicialmente estara parado en un pixel blanco
            #es decir con valor=1
            '''
            1=x-1
            2=x-1,y+1
            3=y+1
            6=x+1,y+1
            9=x+1
            8=x+1,y-1
            7=y-1
            4=x-1,y-1
            
            if y==160 and x==363:
                print 'punto control1';
               
            if y==96 and x==340:
                print 'punto control2';'''
                    
            if veci1==0:
                if x < cordenadaX:
                    if veci4 == 1: 
                        if callejonIzquierdo ==1:
                            if veci9==1:
                                callejonIzquierdo=0;
                                Boundaries.append([y-1,x+1]);
                                x=x+1;
                                y=y-1;
                        else:      
                            Boundaries.append([y,x-1]);
                            x=x-1;
                            y=y;
                    elif veci7 ==1:  
                        Boundaries.append([y-1,x-1]);
                        x=x-1;
                        y=y-1;
                    elif veci8 ==1:
                        if callejonAbajo==1:
                            callejonAbajo=0;
                            Boundaries.append([y+1,x]);
                            x=x;
                            y=y+1; 
                        if callejonArriba==0: 
                            if veci6==1: 
                                Boundaries.append([y-1,x]);
                                x=x;
                                y=y-1;
                            #Es posible que este en medio de
                            #2 caracteres y debe tomar hacia la derecha
                            #o tendera a devolverse al caracter anterior    
                            elif veci6==0:  
                                if veci3 ==1:
                                    #si viene desde abajo
                                    if Boundaries[contador-2][0]>y:
                                        Boundaries.append([y-1,x]);
                                        x=x;
                                        y=y-1;
                                    #si viene desde arriba    
                                    elif Boundaries[contador-2][0]<y:   
                                        Boundaries.append([y+1,x+1]);
                                        x=x+1;
                                        y=y+1; 
                                elif veci3==0:
                                    if veci2==0:
                                        callejonAbajo=1;
                                        Boundaries.append([y-1,x]);
                                        x=x;
                                        y=y-1;
                                    else:
                                        Boundaries.append([y-1,x]);
                                        x=x;
                                        y=y-1;         
                        elif callejonArriba==1:
                            if veci3 ==1:
                                #salgo del callejon 
                                callejonArriba=0;
                                Boundaries.append([y+1,x+1]);
                                x=x+1;
                                y=y+1;
                            elif veci2==1:  
                                Boundaries.append([y+1,x]);
                                x=x;
                                y=y+1;      
                    elif veci9 ==1:
                        Boundaries.append([y-1,x+1]);
                        x=x+1;
                        y=y-1; 
                    elif veci6 ==1:
                        if veci2==0 and Boundaries[contador-2][0]>y:
                            callejonIzquierdo =1; 
                            Boundaries.append([y,x+1]);
                            x=x+1;
                            y=y;
                        else:         
                            Boundaries.append([y,x+1]);
                            x=x+1;
                            y=y;
                    elif veci3 ==1:  
                        Boundaries.append([y+1,x+1]);
                        x=x+1;
                        y=y+1;
                    #Llego a callejon sin salida, debe devolverse    
                    elif veci2 ==1: 
                        callejonArriba=1;
                        Boundaries.append([y+1,x]);
                        x=x;
                        y=y+1;                       
            elif veci2==0:
                if x >0 and y < cordenadaY:    
                    Boundaries.append([y+1,x-1]);
                    x=x-1;
                    y=y+1;
            elif veci3==0:    
                if y < cordenadaY:
                    #si viene desde abajo
                    if Boundaries[contador-2][0]>y:
                        if veci6==1 and veci9==1 and veci8==1:
                            Boundaries.append([y-1,x]); 
                            x=x;
                            y=y-1;
                        else:    
                            Boundaries.append([y+1,x]); 
                            x=x;
                            y=y+1;
                    else:    
                        Boundaries.append([y+1,x]); 
                        x=x;
                        y=y+1;             
            elif veci6==0:
                if x < cordenadaX and y < cordenadaY:    
                    Boundaries.append([y+1,x+1]);
                    x=x+1;
                    y=y+1;
            elif veci9==0:  
                if x < cordenadaX: 
                    Boundaries.append([y,x+1]);
                    x=x+1;
                    y=y;
            elif veci8==0:
                if x < cordenadaX and y > 0:    
                    Boundaries.append([y-1,x+1]);
                    x=x+1;
                    y=y-1;
            elif veci7==0:   
                if y > 0:  
                    Boundaries.append([y-1,x]);
                    x=x;
                    y=y-1;
            elif veci4==0:  
                if x > 0 and y > 0:  
                    Boundaries.append([y-1,x-1]);
                    x=x-1;
                    y=y-1; 
            if x > maxX:
                maxX=x;
            if x < minX:
                minX=x;    
            if y > maxY:
                maxY=y;
            if y < minY:
                minY=y;              
                    
            if x==posicionInicialX and y==posicionInicialY:
                contador=cantidadCoord;
                break;       
    except Exception as e:
        print('Error:'+str(e))
    return Boundaries,minX,minY,maxX,maxY

def Delimitar(PLACA):
    tic = time.time() 
    caracteresT=[];
    caracteres=[];
    anchoCaracter=numpy.zeros((9,1,1),numpy.uint8);
    altoCaracter=numpy.zeros((9,1,1),numpy.uint8);
    posicion=numpy.zeros((9,1,1),numpy.uint8);
    resultado=0
    contador=0
    continuar=0
    w=0
    inicio=1
    cantidadAciertos=0
    #agrego un borde blanco para eliminar el posible marco negro de la placa
    tam=PLACA.shape
    cordenadaY=tam[0]
    cordenadaX=tam[1]
    PLACA=PLACA.clip(0,1)
    
    if cordenadaX > 50 and cordenadaY > 50:
        PLACA=agregarBorde(PLACA,cordenadaX,cordenadaY);
        #numpy.savetxt("placa_detectada2.csv", PLACA, delimiter=",",fmt="%d")
        y_fijo=int(cordenadaY/2);
        topex=int(cordenadaX-(round(cordenadaX*0.1)));
        while inicio < topex and w<=7:
            while PLACA[y_fijo,inicio]==1 and inicio<cordenadaX-1:
                inicio=inicio+1
            
            if y_fijo>0:
                contorno,X_1,Y_1,X_2,Y_2=bwtraceboundary(PLACA,y_fijo,inicio-1,cordenadaY,cordenadaX,1000)            
            
            if len(contorno) > 0: 
                altoCaracter[w]=(Y_2-Y_1+1)
                anchoCaracter[w]=(X_2-X_1+1)
                ancho=(anchoCaracter[w][0][0]/round(cordenadaX))*100
                #delgado=round(cordenadaX*0.13)-anchoCaracter[w][0][0]
                alto=(altoCaracter[w][0][0]/round(cordenadaY))*100
                caracter=PLACA[Y_1+1:Y_2,X_1+1:X_2]
                #numpy.savetxt("caracter"+str(w+1)+".csv",  caracter, delimiter=",",fmt="%d") 
                #print ( 'ancho:' + str(ancho) + 'alto: ' +str(alto) );
                if (ancho >= 9.8 and alto >= 47.8):         
                    caracter=PLACA[Y_1+1:Y_2,X_1+1:X_2]
                    caracter=cv2.resize(caracter,(24,42))
                    caracteres.append(caracter)
                    cantidadAciertos=cantidadAciertos+1
                    #numpy.savetxt("caracter"+str(w+1)+".csv",  caracter, delimiter=",",fmt="%d") 
                inicio=X_2+1
                continuar=1
            else:
                w=9
                continuar=0
                resultado=0
            w=w+1
    else:     
        w=9
        continuar=0
        resultado=0
        
    if len(caracteres)==6:
        #print('Se encontraron los 6 caracteres')
        resultado=1
    #else:
    #    print('cantidad aciertos: '+ str(cantidadAciertos))
            
    tiempoProcesamiento2=time.time() - tic;  
    #print('tiempo en segundos de Delimitacion:'+str(tiempoProcesamiento2))
    return resultado,caracteres,tiempoProcesamiento2

def agregarBorde(PLACA,cordenadaX,cordenadaY):
    #borde izquierdo desde 0 hasta 2% del ancho
    l = numpy.arange(0,int(round(cordenadaX*0.018)),1) 
    PLACA[:,l]=1  
    #borde superior desde 10 % bordehasta fin imagen
    l=numpy.arange(0,int(round(cordenadaY*0.09)),1)
    PLACA[l,:]=1  
    #borde inferior desde 22 %
    desde = cordenadaY-int(round(cordenadaY*0.20)) 
    hasta = cordenadaY
    l=numpy.arange(desde,hasta,1)
    PLACA[l,:]=1  
    #borde derecho
    desde =cordenadaX-int(round(cordenadaX*0.018))
    hasta =cordenadaX
    l=numpy.arange(desde,hasta,1) 
    PLACA[:,l]=1
    #centro
    desde=int((round(cordenadaX/2)-round(cordenadaX*0.025)))
    hasta=int((round(cordenadaX/2)+round(cordenadaX*0.025)))
    l=numpy.arange(desde,hasta,1)
    PLACA[:,l]=1
    return PLACA