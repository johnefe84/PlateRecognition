'''
Created on 21/06/2014

@author: johnefe
'''
import Licencia

class PrincipalCerts:
    
    licencia = Licencia.Licencia()
    licencia.crear_licencia('John Franklin Ruiz Neira',1825)

    if licencia.validar_licencia():
        print('Licencia valida')
    else:
        print('Licencia invalida y/o expirada')    