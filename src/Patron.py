'''
Created on 9/10/2013

@author: johnefe
'''
import numpy   
import time
import cv2
import Segmentacion

def procesarRegion(borde_placa,posicion,total_pixeles,x1,x2,y1,y2,cx,cy):
    #obtengo los centroides del objeto
    objetoCandidato=0
    try:
        #calculo pa proporcion o el aspect ratio
        relacionAspecto=(x2-x1)/(y2-y1)
        #calculo el area segun las cordenadas mas alejadas
        #del borde del objeto para luego compararlo con el
        #area hallada con la funcion determinarArea() y asi poder
        #luego descartar los objetos que no son rectangulos
        #la restriccion de 1000 es para tomar solo imagenes con esa 
        #cantidad minima de pixeles
        
        area1=(y2-y1)*(x2-x1)
        #print ('area1: '+ str(area1))
        if area1 > 7000: 
            #print ('area1: '+ str(area1))
            #Utilizo el teorema de pitagoras para hallar una hipotenusa (a)
            cateto_x=(x2-cx)
            cateto_y=(y2-cy)
            hipotenusa=(cateto_x**2 + cateto_y**2)**(0.5)
            #hipotenusa=int(round(hipotenusa))
            area2 = cv2.contourArea(borde_placa)
            'cateto_x es la distancia entre el borde izquierdo de la placa y el centroide'
            #if hipotenusa > mitad_placa :
            zona=round(round(area2)*100/total_pixeles)
            #divido el area entre el area calculada, si da 1 es por que son iguales
            #area 3 es lado x lado pero utilizando pitagoras. Ver tesis pagina 66
            #print ('hipotenusa: '+ str(hipotenusa)+' cateto_x: '+str(cateto_x))
            if hipotenusa > cateto_x:
                area3=int(4*cateto_x*((hipotenusa**2-cateto_x**2)**0.5))
                #print ('area3: '+ str(area3)+' area2: '+ str(area2)+' area3: '+ str(area1)+' zona : '+ str(zona))
                'Si la similitud entre el area3 y el area2 es mayor al 70% entonces avanza'
                similitud0=abs(round(round(area3*100)/area2))
                #zona el que % ocupa la imagen en toda la foto
                #0.48 es la relacion perfecta de una placa real
                #proporcion es el % de similtud entre la relacion de aspecto 
                #de la placa contra el ideal
                proporcion=abs((0.48 *100)/relacionAspecto)
                #similitud es que tanto se parecen las 2 areas
                #calculadas con diferentes metodos
                similitud1=abs(round(round(area2*100)/area2))
                similitud2=abs(round(round(area1*100)/area2))
                #print('Proporcion alto x ancho= ' +str(proporcion));
                #print('Area 3 lado por lado= ' +str(area3));
                #print('Area 2 count area pixeles= ' +str(area2));
                #print('Zona area2 / total pixeles= ' +str(zona));
                #print('similitud =' +str(similitud));     
                #print('similitud =' +str(similitud2));
                #print('total pixeles =' +str(total_pixeles)); 
                #zonaDetectada=colorDetectadoOri[x1:x2, y1:y2]
                #numpy.savetxt("zona_detectada"+str(posicion)+".csv",  zonaDetectada, delimiter=",",fmt="%d") 
                
                if proporcion >= 90 and similitud1 >= 85 and zona >= 1.8 and similitud2 >= 70:
                    objetoCandidato=proporcion+similitud1+zona+similitud2+similitud0
                    #print('patron encontrado')
                    #print('Proporcion alto x ancho= ' +str(proporcion));
                    #print('Area 1 lado por lado= ' +str(area));
                    #print('Area 2 count area pixeles= ' +str(area2));
                    #print('Zona area2 / total pixeles= ' +str(zona));
                    #print('ladoxlado =' +str(ladoxlado));     
                    #print('total pixeles =' +str(total_pixeles));                  
    except Exception as e:
        print ('Error: '+str(e))
    return objetoCandidato
            
def hallar_esquinas(box,borde_placa,minimo_X):
    sube = 0
    baja = 0
    igual = 0
    diferencia=0
    direccion = ""
    cantidadCoord = borde_placa.shape[0]
    min_Y = min(box[:,0])
    max_Y = max(box[:,0])
    min_X = min(box[:,1])
    max_X = max(box[:,1]) 
    
    longitud=max_X -min_X 
    relacion=0
    pto1x = box[0,0]
    pto2x = box[1,0]
    pto3x = box[2,0]
    pto4x = box[3,0]
    
    pto1y = box[0,1]
    pto2y = box[1,1]
    pto3y = box[2,1]
    pto4y = box[3,1]
    
    for contador in range(0,cantidadCoord):  
        valorY = borde_placa[contador,:,0][0]
        valorX = borde_placa[contador,:,1][0]
        
        if valorX == minimo_X:
            for contador2 in range(contador + 1,cantidadCoord):
                if valorX <= borde_placa[contador2,:,1][0]:
                    if valorY < borde_placa[contador2,:,0][0]:
                        #Si ingresa por aca es por que el siguiente punto es mayor asi que sube
                        sube = sube + 1
                    elif valorY > borde_placa[contador2,:,0][0]:
                        baja = baja + 1
                    else:    
                        igual = igual +1
            diferencia= sube-baja
            relacion=(float(diferencia)/float(longitud))*100
            if relacion > 40 and sube > baja:
                direccion = "LADEADA_DERECHA"
                punto3x = buscar_parejaY(min_Y,box)
                punto3y = min_Y
                punto1y = buscar_parejaX(min_X,box)
                punto1x = min_X
                punto4y = buscar_parejaX(max_X,box)
                punto4x = max_X
                punto2x = buscar_parejaY(max_Y,box)
                punto2y = max_Y
                #print("punto1(x,y) : (" + str(punto1x) + "," + str(punto1y) + ")") 
                #print("punto2(x,y) : (" + str(punto2x) + "," + str(punto2y) + ")") 
                #print("punto3(x,y) : (" + str(punto3x) + "," + str(punto3y) + ")")
                #print("punto4(x,y) : (" + str(punto4x) + "," + str(punto4y) + ")")
            elif relacion < -15 and baja > sube:
                direccion = "LADEADA_IZQUIERDA"
                punto1x = buscar_parejaY(min_Y,box)
                punto1y = min_Y
                punto2y = buscar_parejaX(min_X,box)
                punto2x = min_X
                punto3y = buscar_parejaX(max_X,box)
                punto3x = max_X
                punto4x = buscar_parejaY(max_Y,box)
                punto4y = max_Y
                #print("punto1(x,y): (" + str(punto1x) + "," + str(punto1y) + ")") 
                #print("punto2(x,y): (" + str(punto2x) + "," + str(punto2y) + ")") 
                #print("punto3(x,y): (" + str(punto3x) + "," + str(punto3y) + ")")
                #print("punto4(x,y): (" + str(punto4x) + "," + str(punto4y) + ")") 
            else:
                direccion = "RECTA"     
                punto4x = max_X
                punto4y = max_Y
                punto3y = max_Y
                punto3x = min_X
                punto2y = min_Y
                punto2x = max_X
                punto1x = min_X
                punto1y = min_Y
                #print("punto1(x,y)-: (" + str(punto1x) + "," + str(punto1y) + ")") 
                #print("punto2(x,y)-: (" + str(punto2x) + "," + str(punto2y) + ")") 
                #print("punto3(x,y)-: (" + str(punto3x) + "," + str(punto3y) + ")")
                #print("punto4(x,y)-: (" + str(punto4x) + "," + str(punto4y) + ")") 
        else:
            direccion = "RECTA"     
            punto4x = max_X
            punto4y = max_Y
            punto3y = max_Y
            punto3x = min_X
            punto2y = min_Y
            punto2x = max_X
            punto1x = min_X
            punto1y = min_Y  
        break
    #print(direccion + ' diferencia: '+str(relacion))
    return punto1x,punto1y,punto2x,punto2y,punto3x,punto3y,punto4x,punto4y,direccion         

def buscar_parejaX(coordenadaX,box):
    
    #promedio = 0
    #contador = 0
    
    for contador in range(0,4):
        valorX = box[contador,1]
        valorY = box[contador,0]
        
        if valorX == coordenadaX:
            break
            #promedio=promedio+valorY
            #contador=contador+1
        
    return valorY

def buscar_parejaY(coordenadaY,box):
    
    for contador in range(0,4):
        valorX = box[contador,1]
        valorY = box[contador,0]
        
        if valorY == coordenadaY:
            break
        
    return valorX

            
def buscarPatron(colorDetectado,fotoOriginal,ancho,alto):
    tic = time.time()          
    resultado=0
    coordenadas=numpy.zeros((1,4,2))
    total_pixeles=ancho*alto
    posicion=0 
    punto1x=0
    punto1y=0
    punto2x=0
    punto2y=0
    punto3x=0
    punto3y=0
    punto4x=0
    punto4y=0
        #hierarchy =[Next, Previous, First_Child, Parent]
        #http://opencvpython.blogspot.com/2013/01/contours-5-hierarchy.html
    try:
        cv2.imshow('colorDetectado',colorDetectado)

        Boundaries,hierarchy = cv2.findContours(colorDetectado,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cantidad_objetos = 0
        if hierarchy.shape[1] > 0:
            cantidad_objetos=hierarchy.shape[1]
        else:
            cantidad_objetos=0

    except Exception as e:
        print('Error findContours : '+str(e))
    # estadistica almacena el area y centroide de cada region
    if len(Boundaries)>0:
        objetosCandidatos=numpy.zeros((cantidad_objetos,1,1),numpy.uint8);
        while posicion != cantidad_objetos:
            continuar = True
            borde_placa = Boundaries[posicion];
            #print(borde_placa)
            #cv2.waitKey(0)
            if len(borde_placa) > 3:
                #Obtengo el valor de los pixeles que estan mas alejados
                #en el contorno del objeto
                y1 = float(min(borde_placa[:,:,0]))
                y2 = float(max(borde_placa[:,:,0]))
                x1 = float(min(borde_placa[:,:,1]))
                x2 = float(max(borde_placa[:,:,1])) 
                M = cv2.moments(borde_placa)
                #Busqueda del centroide de la region
                if int(M['m00'])>0 and int(M['m00'])>0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    if (x1 == 0 or y1 == 0 or x2==ancho or y2==alto or (x2-x1)==0 or (y2-y1)==0):
                        continuar = False
                else:
                    continuar = False    
            #validar si el objeto esta en el borde de la imagen    
            else:
                continuar = False

            if continuar: 
                objetoCandidato=procesarRegion(borde_placa,posicion,total_pixeles,x1,x2,y1,y2,cx,cy)

                if objetoCandidato != 0:
                    print("objetoCandidato ok ",objetoCandidato)
                    objetosCandidatos[posicion]=objetoCandidato

            posicion=posicion+1
        #Analisis de todos los candidatos para determinar el mejor
        valorMaximo=max(objetosCandidatos)
        candidatoMax=list(objetosCandidatos).index(valorMaximo)
            
        if candidatoMax>=0 and len(objetosCandidatos)>0 and valorMaximo > 0: 
            borde_placa= Boundaries[candidatoMax];
            y1 = float(min(borde_placa[:,:,0]))
            y2 = float(max(borde_placa[:,:,0]))
            x1 = float(min(borde_placa[:,:,1]))
            x2 = float(max(borde_placa[:,:,1]))
            resultado=1
            rect = cv2.minAreaRect(borde_placa)
            box = cv2.cv.BoxPoints(rect)
            box = numpy.int0(box)
            punto1x,punto1y,punto2x,punto2y,punto3x,punto3y,punto4x,punto4y,direccion=hallar_esquinas(box,borde_placa,int(x1))

            if direccion == 'LADEADA_DERECHA' or direccion == 'LADEADA_IZQUIERDA':
                pts1 = numpy.float32([[punto1y,punto1x],[punto2y,punto2x],[punto3y,punto3x],[punto4y,punto4x]])
                pts2 = numpy.float32([[10,10],[(punto2y-punto1y),10],[10,(punto4x-punto2x)],[(punto2y-punto1y),(punto4x-punto2x)]])
                placaDetectada2=Segmentacion.transformar(fotoOriginal,ancho,alto,pts1,pts2)
                placaDetectada2=placaDetectada2[10:(punto4x-punto2x),10:(punto2y-punto1y)]  
            else:
                placaDetectada2=fotoOriginal[x1:x2, y1:y2]    
            #numpy.savetxt("placa_detectada1.csv",  placaDetectada2, delimiter=",",fmt="%d")
        else:
            resultado=0
            placaDetectada2=fotoOriginal
    else:
        resultado=0
        placaDetectada2=fotoOriginal

    if resultado==0:
        borde_placa=numpy.zeros((2,1,2))

    cv2.imshow('placaDetectada2',placaDetectada2)
    cv2.waitKey(0)
    tam=placaDetectada2.shape
    ancho=tam[0]
    alto=tam[1]
    if ancho == 0 or alto == 0:
        placaDetectada2=fotoOriginal
        #print('sin placa')
    tiempoProcesamiento1=time.time() - tic; 
    return resultado, placaDetectada2, tiempoProcesamiento1

def validacion(arreglo):
    return numpy.sum(arreglo, axis=1)

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray