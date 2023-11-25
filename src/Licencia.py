'''
Created on 21/06/2014

@author: johnefe
'''

#import Serial 
import Consulta_BD
import subprocess 
import os
import time
import datetime
import win32api

class Licencia: 

    def get_serial_pc2(self):
        x = win32api.GetVolumeInformation('C:\\')
        volser = int(x[1])
        
        volser = 4294967296 - abs(volser)
        data = hex(volser).strip('L').upper()[2:]
        '''
        while len(data) < 8:
            data = '0' + data
            print 'Serial # for drive %s is %4s %4s' %('C', data[0:-4],data[-4:])
            data =data[0:-4]
        '''    
        #data=str(data).encode('base64','strict')
        return data
        
    def get_serial_pc(self):
        data = os.popen('vol '+'c:', 'r').read()
        data = data.split(':')[1]
        data=data.rstrip('\n')
        #print data
        #data=str(data).encode('base64','strict')
        return data
    
    def get_serial_certificado(self):
        #st_cert=open(certificado, 'rt').read()
        #cert=crypto.load_certificate(crypto.FILETYPE_PEM, st_cert)
        #common_name=cert.get_subject().CN 
        #serial=cert.get_subject().O 
        subject=subprocess.check_output("openssl x509 -in certs/licencia.lic -noout -subject",shell=True)
        partes=subject.split('=', 3 );
        serial=partes[3]
        common_name=partes[2][:-2]
        return common_name,serial
    
    def fecha_expiracion(self):
        expira=subprocess.check_output("openssl x509 -in certs/licencia.lic -noout -enddate",shell=True)
        #notAfter=Jul 23 20:09:31 2014 GMT 
        partes=expira.split('=', 1 );
        resultado=partes[1][:-4]
        partes2=resultado.split(' ', 4 );
        resultado=partes2[1]+' '+partes2[0]+' '+partes2[3]
        return resultado
     
    def fecha_expiracion2(self):
        expira=subprocess.check_output("openssl x509 -in certs/licencia.lic -noout -enddate",shell=True)
        #notAfter=Jul 23 20:09:31 2014 GMT 
        partes=expira.split('=', 1 );
        resultado=partes[1][:-4]
        partes2=resultado.split(' ', 4 );
        # Para windows xp y 7
        #resultado=partes2[1]+' '+partes2[0]+' '+partes2[3]
        resultado=partes2[2]+' '+partes2[0]+' '+partes2[4]
        return resultado.strip(" ")
    
      
    
    def crear_licencia(self,cliente,dias,anos):
        import OpenSSL.crypto as crypto
        import certgen 
        #cliente='Marcela Ayala Balaguera'
        cacert=certgen.readCertificate('certs/CA.lic')
        cakey=certgen.readKeyCertificate('certs/CA.key')
        serial=self.get_serial_pc2()
        pkey = certgen.createKeyPair(certgen.TYPE_RSA, 1024)
        req = certgen.createCertRequest(pkey, CN=cliente,O=serial)
        cert = certgen.createCertificate(req, (cacert, cakey), 1, (0, 60*60*24*int(dias)*int(anos)*1)) 
        open('certs/%s.key' % ('licencia',), 'w').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
        open('certs/%s.lic' % ('licencia',), 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        
    def crear_licencia_remota(self,cliente,dias,anos,serial):
        import OpenSSL.crypto as crypto
        import certgen 
        #cliente='Marcela Ayala Balaguera'
        cacert=certgen.readCertificate('certs/CA.lic')
        cakey=certgen.readKeyCertificate('certs/CA.key')
        pkey = certgen.createKeyPair(certgen.TYPE_RSA, 1024)
        req = certgen.createCertRequest(pkey, CN=cliente,O=serial)
        cert = certgen.createCertificate(req, (cacert, cakey), 1, (0, 60*60*24*int(dias)*int(anos)*1)) 
        open('certs/%s.key' % ('licencia',), 'w').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
        open('certs/%s.lic' % ('licencia',), 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    
    def validar_licencia_remota(self,serial_pc_actual):  
        #st_cert=open('certs/licencia.lic', 'rt').read()
        #cert=crypto.load_certificate(crypto.FILETYPE_PEM, st_cert)
        try:
            fecha_expira=datetime.datetime(*time.strptime(self.fecha_expiracion(), "%d %b %Y")[0:6])
        except:
            fecha_expira=datetime.datetime(*time.strptime(self.fecha_expiracion2(), "%d %b %Y")[0:6])
            
        fecha_actual=datetime.datetime(*time.strptime(time.strftime("%d/%m/%Y"), "%d/%m/%Y")[0:6])
        
        if (fecha_expira >= fecha_actual):
        #expiro=cert.has_expired()
            expiro=0
        else:
            expiro=1
                
        retorno=False
        
        if (expiro==0):
            #print('Licencia valida!')
            #print('Common_name: ' + nombre)
            #print('Serial Disco: '+ ser)
            #Se valida que no se haya modificado la fecha del sistema
            consulta = 'select  count(*) from servicio_parqueo where CURDATE() >= fecha_ingreso'
            valor, count_consulta, resultado=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
            if valor == 1 and count_consulta>0:
                cantidad=resultado.fetchone()[0]
                if cantidad >0:
                    #Se verifica si la licencia fue generada por la CA
                    resultado=subprocess.check_output("openssl verify -CAfile certs/CA.lic certs/licencia.lic", shell=True)
                    #resultado=os.system('openssl verify -CAfile certs/CA.lic certs/licencia.lic')
                    print(resultado);
                    cantidad=str(resultado).find('OK')
                    if cantidad > 0:
                        retorno=True
                        expira=self.fecha_expiracion()
                        print('La licencia expira: '+expira)
                    else:
                        print('La licencia no es original');
                        retorno=False    
                else:
                    print ('Se modifico la fecha del sistema. Posible fraude!')
                    retorno=False    
            else:
                #Si es un sistema nuevo y la tabla esta vacia
                consulta = 'select  count(*) from servicio_parqueo'
                valor, count_consulta, resultado=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                if valor == 1 and count_consulta==0:
                    cantidad=resultado.fetchone()[0]
                    if cantidad >0:
                        #Se verifica si la licencia fue generada por la CA
                        resultado=subprocess.check_output("openssl verify -CAfile certs/CA.lic certs/licencia.lic", shell=True)
                        #resultado=os.system('openssl verify -CAfile certs/CA.lic certs/licencia.lic')
                        print(resultado);
                        cantidad=str(resultado).find('OK')
                        if cantidad > 0:
                            retorno=True
                            print('La licencia expira: '+str(fecha_expira))
                        else:
                            print('La licencia no es original');
                            retorno=False    
                    else:
                        print ('Se modifico la fecha del sistema. Posible fraude!')
                        retorno=False    
                 
        else:
            print('Licencia expiro!')  
            retorno=False
   
        return retorno     
    def validar_licencia(self):
        serial_pc_actual=self.get_serial_pc2()   
        nombre,ser=self.get_serial_certificado()
        st_cert=open('certs/licencia.lic', 'rt').read()
        try:
            fecha_expira=datetime.datetime(*time.strptime(self.fecha_expiracion(), "%d %b %Y")[0:6])
        except:
            fecha_expira=datetime.datetime(*time.strptime(self.fecha_expiracion2(), "%d %b %Y")[0:6])
            
        fecha_actual=datetime.datetime(*time.strptime(time.strftime("%d/%m/%Y"), "%d/%m/%Y")[0:6])
        
        if (fecha_expira >= fecha_actual):
        #expiro=cert.has_expired()
            expiro=0
        else:
            expiro=1
                
        retorno=False
        
        if (serial_pc_actual.strip()==ser.strip()):
            if (expiro==0):
                #print('Licencia valida!')
                #print('Common_name: ' + nombre)
                #print('Serial Disco: '+ ser)
                #Se valida que no se haya modificado la fecha del sistema
                consulta = 'select  count(*) from servicio_parqueo where CURDATE() >= fecha_ingreso'
                valor, count_consulta, resultado=Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                if valor == 1 and count_consulta>0:
                    cantidad=resultado.fetchone()[0]
                    if cantidad >0:
                        #Se verifica si la licencia fue generada por la CA
                        resultado=subprocess.check_output("openssl verify -CAfile certs/CA.lic certs/licencia.lic", shell=True)
                        #resultado=os.system('openssl verify -CAfile certs/CA.lic certs/licencia.lic')
                        print(resultado);
                        cantidad=str(resultado).find('OK')
                        if cantidad > 0:
                            retorno=True
                            print('La licencia expira: '+str(fecha_expira))
                        else:
                            print('La licencia no es original');
                            retorno=False    
                    else:
                        print ('Se modifico la fecha del sistema. Posible fraude!')
                        retorno=False     
            else:
                print('Licencia expiro!')  
                retorno=False
        else:
            print('Licencia no autorizada para este equipo! -'+serial_pc_actual.strip()+"-"+ser.strip()+"-") 
            retorno=False    
        return retorno     