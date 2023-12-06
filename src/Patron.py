'''
Created on 9/10/2013

@author: johnefe
'''
import numpy   
import time
import cv2
import Segmentacion
import math

"""
_0_|x1______x2_
 y1|
   |
   |
 y2|
"""

MOSTRAR_TODOS_BORDES = False
MOSTRAR_CANDIDATOS = False
MOSTRAR_FINALES = True

def procesarRegionParaHallarPosiblesLetras(borde_placa,posicion,total_pixeles,x1,x2,y1,y2,cx,cy):
    objetoCandidato=0
    try:
        relacionAspecto = (y2-y1)/(x2-x1)
        area=(y2-y1)*(x2-x1)

        if(relacionAspecto >= 0.4 and relacionAspecto <= 0.86 and area/total_pixeles >= 0.008 and area/total_pixeles <= 0.3):
            objetoCandidato = relacionAspecto;
        
    except Exception as e:
        print ('Error: '+str(e))
    return objetoCandidato

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
        #if area1 > 7000: 
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
            #0.48 es la relacion perfecta de una placa real (la placa colombiana mide oficialmente 330 mmm de largo por 16 mm de ancho) 160/330=0.48 
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
            
            if proporcion >= 90 and similitud1 >= 85 and similitud1 <= 100 and similitud2 >= 70 and similitud2 <= 100 and zona >= 2:
                objetoCandidato=proporcion+similitud1+similitud2+similitud0
                #print('patron encontrado')
                #print('Proporcion alto x ancho= ' +str(proporcion));
                #print('Area 1 lado por lado= ' +str(area));
                #print('Area 2 count area pixeles= ' +str(area2));
                #print('Zona area2 / total pixeles= ' +str(zona));
                #print('lado x lado =' +str(ladoxlado));     
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

            
def buscarPatron(imagenBinaria,fotoOriginal,ancho,alto, FotoOriginal):
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
        Boundaries,hierarchy = cv2.findContours(imagenBinaria,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        if(MOSTRAR_TODOS_BORDES):
            for c in Boundaries:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(FotoOriginal, (x, y), (x+w, y+h), (255, 0, 255), 2)
                #cv2.putText(FotoOriginal,str(y) ,(x,y+h),0,0.5,(0,255,0))
                cv2.imshow('Bounding Rectangle', FotoOriginal)
            cv2.waitKey(0)

        cantidad_objetos = 0
        if hierarchy.shape[1] > 0:
            cantidad_objetos=hierarchy.shape[1]

        else:
            cantidad_objetos=0

    except Exception as e:
        print('Error findContours : '+str(e))
    # estadistica almacena el area y centroide de cada region
    if len(Boundaries)>0:
        objetosCandidatos = numpy.ones((cantidad_objetos,1,1),numpy.int32)*-1;
        objetoEncontrado = False
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
                objetoCandidato = procesarRegionParaHallarPosiblesLetras(borde_placa,posicion,total_pixeles,x1,x2,y1,y2,cx,cy)
                #objetoCandidato=procesarRegion(borde_placa,posicion,total_pixeles,x1,x2,y1,y2,cx,cy)

                if objetoCandidato != 0:
                    objetoEncontrado = True
                    #print("objetoCandidato ok ",objetoCandidato)
                    objetosCandidatos[posicion] = posicion


            posicion=posicion+1
        #Nuevo metodo para ver si los objetos candidatos esta cerca de otro sobre una linea horizontal o inclinada, asi encontrare los
        #que estan cerca y que deben ser los caracteres
        #if (objetoEncontrado):
        #    calcularAnguloDiagonalConRespectoEjeX(Boundaries,objetosCandidatos,FotoOriginal)


        #Analisis de todos los candidatos para determinar el mejor
        #valorMaximo=max(objetosCandidatos)
        #candidatoMax=list(objetosCandidatos).index(valorMaximo)
        elementosFinales = metricasCaracter(Boundaries, objetosCandidatos, FotoOriginal)    
        
        """"
        if candidatoMax>=0 and len(objetosCandidatos)>0 and valorMaximo > 0: 
            borde_placa= Boundaries[candidatoMax];
            y1 = float(min(borde_placa[:,:,0]))
            y2 = float(max(borde_placa[:,:,0]))
            x1 = float(min(borde_placa[:,:,1]))
            x2 = float(max(borde_placa[:,:,1]))
            resultado=1
            rect = cv2.minAreaRect(borde_placa)
            box = cv2.boxPoints(rect)
            box = numpy.int0(box)
            punto1x,punto1y,punto2x,punto2y,punto3x,punto3y,punto4x,punto4y,direccion=hallar_esquinas(box,borde_placa,int(x1))

            if direccion == 'LADEADA_DERECHA' or direccion == 'LADEADA_IZQUIERDA':
                pts1 = numpy.float32([[punto1y,punto1x],[punto2y,punto2x],[punto3y,punto3x],[punto4y,punto4x]])
                pts2 = numpy.float32([[10,10],[(punto2y-punto1y),10],[10,(punto4x-punto2x)],[(punto2y-punto1y),(punto4x-punto2x)]])
                placaDetectada2=Segmentacion.transformar(fotoOriginal,ancho,alto,pts1,pts2)
                placaDetectada2=placaDetectada2[10:(punto4x-punto2x),10:(punto2y-punto1y)]  
            else:
                placaDetectada2=fotoOriginal[int(x1):int(x2), int(y1):int(y2)]    
                #numpy.savetxt("placa_detectada1.csv",  placaDetectada2, delimiter=",",fmt="%d")
        else:
            resultado=0
            placaDetectada2=fotoOriginal
        """
        placaDetectada2=fotoOriginal
    else:
        resultado=0
        placaDetectada2=fotoOriginal

    if resultado==0:
        borde_placa=numpy.zeros((2,1,2))

    #cv2.imshow('placaDetectada2',placaDetectada2)
    #cv2.waitKey(0)
    tam=placaDetectada2.shape
    ancho=tam[0]
    alto=tam[1]
    if ancho == 0 or alto == 0:
        placaDetectada2=fotoOriginal
        #print('sin placa')
    tiempoProcesamiento1=time.time() - tic; 
    return resultado, placaDetectada2, tiempoProcesamiento1

def metricasCaracter(Boundaries, objetosCandidatos, FotoOriginal):
    anchoTotalImagen = FotoOriginal.shape[1]
    alturaTotalImagen = FotoOriginal.shape[0]
    """
    box coordenadas empieza en esquina superior izquierda y avanza en sentido horario x,y
    1--2
    |  |
    4--3
    """
    metricasCaracterList=[]
    elementosABorrar=[]
    elementosFinales=[]

    for objetoCandidato in objetosCandidatos:
        if(objetoCandidato[0][0] > 0):
            borde_caracter = Boundaries[int(objetoCandidato)]            
            #rect = cv2.minAreaRect(borde_caracter)
            #box = cv2.boxPoints(rect)
            x,y,ancho,alto = cv2.boundingRect(borde_caracter)
            porcentajeDistanciaBordeInferiorImagen = (alturaTotalImagen-alto/alturaTotalImagen)*100
            metricasCaracterList.append(CaracterMetricas(ancho, alto, False, porcentajeDistanciaBordeInferiorImagen, list(objetosCandidatos).index(objetoCandidato),x,(x+ancho),y,(y+alto)))
    
    metricasCaracterList.sort(key = evaluacionOrdenamiento2)
    for index in range(0,len(metricasCaracterList)-1):
        if(index==3):
            print("parar")
        metrica = metricasCaracterList[index]
        filtrados = list(filter(lambda b: (b.ancho <= metrica.ancho*1.5), metricasCaracterList))
        metricasCaracterList[index].hayMasIgualAnchos = len(filtrados)
        filtrados = list(filter(lambda b: (b.alto <= metrica.alto*1.5), metricasCaracterList))
        metricasCaracterList[index].hayMasIgualAltos = len(filtrados)
        filtrados = list(filter(lambda b: (b.porcentajeDistanciaBordeInferiorImagen*1.1 >= (metrica.porcentajeDistanciaBordeInferiorImagen)), metricasCaracterList))
        metricasCaracterList[index].hayMasSimilarUbicacionY = len(filtrados)
        existeCaracterAlaDerecha= (metrica.x1*1,3 <= metricasCaracterList[index+1].x2)
        metricasCaracterList[index].boundarieXContiguo = existeCaracterAlaDerecha
        filtrados = list(filter(lambda b: ((metrica.x1 < b.x1) and (metrica.x2 > b.x2) and (metrica.y1 < b.y1) and (metrica.y2 > b.y2)), metricasCaracterList))
        metricasCaracterList[index].tieneCaracteresPorDentro = filtrados

    for index in range(0,len(metricasCaracterList)):
        metrica = metricasCaracterList[index]
        if(metrica.posicionArray==1804):
            print("parar debug")
        if(metrica.x1 == 0 or metrica.x2 == anchoTotalImagen-1 or metrica.y1 == 0 or metrica.y2 == alturaTotalImagen-1):
            elementosABorrar.append(metrica.posicionArray)
        if(metrica.hayMasIgualAnchos < 4 and metrica.hayMasIgualAltos < 4 and metrica.boundarieXContiguo == False and metrica.hayMasSimilarUbicacionY < 4):
            elementosABorrar.append(metrica.posicionArray)
        for elemento in metrica.tieneCaracteresPorDentro:
            elementosABorrar.append(elemento.posicionArray)            

    for index in range(0, len(metricasCaracterList)):
        elemento = metricasCaracterList[index]
        encontrado = False
        for b in elementosABorrar:
            if b == elemento.posicionArray:
                encontrado = True
        if(encontrado == False):
            elementosFinales.append(elemento)

    if (MOSTRAR_FINALES):
        for index in range(0, len(elementosFinales)):
            objeto = elementosFinales[index]
            x,y,w,h = cv2.boundingRect(Boundaries[objeto.posicionArray])
            cv2.rectangle(FotoOriginal, (x, y), (x+w, y+h), (255, 0, 255), 2)
            cv2.putText(FotoOriginal,str(objeto.posicionArray) ,(x,y+h),0,0.5,(0,255,0))
            cv2.imshow('Bounding Rectangle', FotoOriginal)
        cv2.waitKey(0) 
    return elementosFinales

def validacion(arreglo):
    return numpy.sum(arreglo, axis=1)

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def calcularAnguloDiagonalConRespectoEjeX(Boundaries,objetosCandidatos,FotoOriginal):
    ObjetoCandidatoList = []
    for objetoCandidato in objetosCandidatos:
        if(objetoCandidato[0][0] > 0):
            borde_placa = Boundaries[int(objetoCandidato)]
            #en el contorno del objeto
            y1 = float(min(borde_placa[:,:,0]))
            y2 = float(max(borde_placa[:,:,0]))
            x1 = float(min(borde_placa[:,:,1]))
            x2 = float(max(borde_placa[:,:,1]))
            hipotenusa=((x2-x1)**2 + (y2-y1)**2)**(0.5) 
            angulo = math.acos(math.cos(1/((x2-x1)/hipotenusa)))
            ObjetoCandidatoList.append(ObjetoCandidatoClass(int(objetoCandidato), angulo, x1, y1))
            ObjetoCandidatoList.sort(key = evaluacionOrdenamiento)

    #lineas = caclularLineas(ObjetoCandidatoList)
    i = 0
    """
        self.ancho = ancho
        self.alto = alto
        self.tieneCaracteresPorDentro = []
        self.boundarieXContiguo = boundarieXContiguo
        self.porcentajeDistanciaBordeInferiorImagen = porcentajeDistanciaBordeInferiorImagen
        self.posicionArray = posicionArray
        self.hayMasIgualAnchos = 0
        self.hayMasIgualAltos = 0
        self.hayMasSimilarUbicacionY = 0
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    """
    for objeto in ObjetoCandidatoList:
        #if((i+2) < len(ObjetoCandidatoList)):
            #esLinear = collinear(ObjetoCandidatoList[i],ObjetoCandidatoList[i+1],ObjetoCandidatoList[i+2])
            #print(esLinear)
            #if(esLinear):
        if(MOSTRAR_CANDIDATOS):
            x,y,w,h = cv2.boundingRect(Boundaries[objeto.posicion])
            cv2.rectangle(FotoOriginal, (x, y), (x+w, y+h), (255, 0, 255), 2)
            #cv2.putText(FotoOriginal,str(len(objeto.angulo)) ,(x,y+h),0,0.5,(0,255,0))
            cv2.imshow('Bounding Rectangle', FotoOriginal)
        i = i+1
        cv2.waitKey(0) 
    
    print("termine")

def evaluacionOrdenamiento(e):
    return e.coordenada[1]

def evaluacionOrdenamiento2(e):
    return e.x1

# get the y=mx+c equation from given points
def get_slope_and_intercept(pointA, pointB):
    slope = (pointB[1] - pointA[1])/(pointB[0] - pointA[0])
    intercept = pointB[1] - slope * pointB[0]
    return slope, intercept

# a simple algorithm to find the hash of slope and intercept
def get_unique_id(slope, intercept):
    return str(slope)+str(intercept)

def caclularLineas(pointsWithObjects):
    points = []
    for objeto in pointsWithObjects:
        points.append(objeto.coordenada)    
    
    lines = []
    hash_table = []
    for A in pointsWithObjects:
        for B in pointsWithObjects:
            if A.coordenada[0] != B.coordenada[1] and A.coordenada[0] != B.coordenada[1]: #not matching the same points
                #find the equation of line
                slope, intercept = get_slope_and_intercept(A.coordenada, B.coordenada)
                line = [A.coordenada, B.coordenada]
                unique_hash = get_unique_id(slope, intercept)
                if unique_hash not in hash_table:
                    hash_table.append(unique_hash)
                    for C in points:
                        if B.coordenada[1] != C[0] and B.coordenada[1] != C[1] and A.coordenada[0] != C[0] and A.coordenada[1] != C[1]:
                            # check if this point lies on the same line as A and B
                            # y - mx - c = 0
                            rhs = C[1] - slope * C[0] - intercept
                            if rhs >= 0 and rhs <= 9:
                                line.append(C)
                    # finally append whatever is found to be in one line, more than 2 points
                    if len(line) > 2:
                        lines.append(line)
                        #lines.append(ObjetoCandidatoClass(list(pointsWithObjects).index(valorMaximo))line)
    print("lines")
    print(lines)
    return lines 

def collinear(objetoCandidato1, objetoCandidato2, objetoCandidato3):
    x1 = objetoCandidato1.coordenada[0]
    y1 = objetoCandidato1.coordenada[1]
    x2 = objetoCandidato2.coordenada[0]
    y2 = objetoCandidato2.coordenada[1]
    x3 = objetoCandidato3.coordenada[0]
    y3 = objetoCandidato3.coordenada[1]

    pendiente1 = calcularPendiente(x1,y1,x2,y2)
    pendiente2 = calcularPendiente(x2,y2,x3,y3)
    pendiente3 = calcularPendiente(x1,y1,x3,y3)

    if (pendiente2 >0):
        if((((pendiente1/pendiente2)*100) > 90 and ((pendiente1/pendiente2)*100) < 110)):
            if (pendiente3 >0):
                if((((pendiente1/pendiente3)*100) > 90 and ((pendiente1/pendiente3)*100) < 110)):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

def calcularPendiente(x1,y1,x2,y2):
    pendiente=0
    if (y2>y1):
        deltaY1 = (y2-y1)
    else:
        deltaY1 = (y1-y2)
    
    if (x2>x1):
        deltaX1 = (x2-x1)
    else:
        deltaX1 = (x1-x2)

    if(deltaX1 >0):
        pendiente = deltaY1/deltaX1

    return pendiente

class ObjetoCandidatoClass():
    def __init__(self, posicion, angulo, x, y):
        self.posicion = posicion
        self.angulo = angulo
        self.coordenada = [x,y]

class CaracterMetricas():
    def __init__(self, ancho, alto, boundarieXContiguo, porcentajeDistanciaBordeInferiorImagen, posicionArray, x1, x2, y1, y2):
        self.ancho = ancho
        self.alto = alto
        self.tieneCaracteresPorDentro = []
        self.boundarieXContiguo = boundarieXContiguo
        self.porcentajeDistanciaBordeInferiorImagen = porcentajeDistanciaBordeInferiorImagen
        self.posicionArray = posicionArray
        self.hayMasIgualAnchos = 0
        self.hayMasIgualAltos = 0
        self.hayMasSimilarUbicacionY = 0
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2