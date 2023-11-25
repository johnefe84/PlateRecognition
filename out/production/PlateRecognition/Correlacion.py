'''
Created on 5/01/2014

@author: johnefe
'''
import numpy

def corr2(matrizA,matrizB):
    Amedia=numpy.mean(matrizA);
    Bmedia=numpy.mean(matrizB);
    numerador = 0;
    denominador1=0;
    denominador2=0;
    tamano=matrizA.shape;
    tamano2=matrizB.shape;
    x=tamano[0];
    y=tamano[1];
    x2=tamano[0];
    y2=tamano[1];
    
    if x==x2 and y==y2:
        for i in range(0,x):
            for j in range(0,y):
                a =(matrizA[i,j]-Amedia);
                b =(matrizB[i,j]-Bmedia);
                total1=a*b;
                numerador = numerador+total1;
                total2=a**2;
                denominador1=denominador1+total2
                total3=b**2;
                denominador2=denominador2+total3
        denominador=(denominador1*denominador2)**0.5;
        corr=float(numerador/denominador);
        return corr
    else:
        print('Las dos matrices no son del mismo tamamo')
        return 0;
'''
matrizA=[]
matrizB=[]

matrizA.append([0,0,0,0,0])
matrizA.append([0,1,1,1,0])
matrizA.append([0,1,0,0,0])
matrizA.append([0,1,1,1,0])
matrizA.append([0,0,0,1,0])
matrizA.append([0,1,1,0,0])
matrizA.append([0,0,0,0,0])
arrayA=numpy.array(matrizA)

matrizB.append([0,0,0,0,0])
matrizB.append([0,1,1,1,0])
matrizB.append([0,1,0,0,0])
matrizB.append([0,1,1,1,0])
matrizB.append([0,1,0,1,0])
matrizB.append([0,1,1,1,0])
matrizB.append([0,0,0,0,0])
arrayB=numpy.array(matrizB)

correlacion=corr2(arrayA,arrayB)
if correlacion <>0:
    print('La correlacion es:'+str(correlacion))'''
    