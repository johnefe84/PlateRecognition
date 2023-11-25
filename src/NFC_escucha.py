'''
Modificado on 20/08/2014

@author: johnefe
'''
#!/usr/bin/env python

"""

MIFARE RFID tag read/write utility for ACS ACR122 writer

Source code put in public domain by Didier Stevens, no Copyright
https://DidierStevens.com
Use at your own risk

History:
  2009/02/17: start
  2009/02/18: writefile
  2009/02/19: shellcode execution

Todo:
  - support other types than MIFARE 1K tags
"""

__author__ = 'Didier Stevens'
__version__ = '0.0.1'
__date__ = '2009/02/19'

import smartcard.System
import smartcard.util
import smartcard.CardConnection
import optparse
#import pyttsx
import time
import Licencia
import Consulta_BD
import numpy
import ControlUSB

DEFAULT_KEYA = 'FFFFFFFFFFFF'

def ReadBinaryFile(name):
    try:
        fBinary = open(name, 'rb')
    except:
        return None
    try:
        return fBinary.read()
    except:
        return None
    finally:
        fBinary.close()
    return None

def WriteBinaryFile(name, content):
    try:
        fBinary = open(name, 'wb')
    except:
        return False
    try:
        fBinary.write(content)
    except:
        return False
    finally:
        fBinary.close()
    return True

class cMIFARE:
    cantidadLectores=0
    
    def __init__(self,unidad):
        self.smartCardReader=self.getReader(unidad)
        #self.smartCardReader = self.GetSmartCardReader()
        if str(self.smartCardReader) == '':
            print 'No se encontro lector ACS ACR122'
            exit()
               
        print 'Lector: %s' % self.smartCardReader
        self.KeyBlockNumber = None
        
    def getReader(self,unidad):
        readers = smartcard.System.readers()
        cantidad=0
        if len(readers) == 1:
            return readers[0]
        elif len(readers) == 0:
            return ''
        else:
            for r in readers:
                if str(r).upper().find('ACR122') > -1:
                    if cantidad==unidad:
                        return r
                    cantidad=cantidad+1    

    def GetSmartCardReader(self):
        """
           If only one reader connected, return that reader.
           If more than one reader is connected, return the first reader with the string ACR122"""
           
        readers = smartcard.System.readers()
        if len(readers) == 1:
            return readers[0]
        elif len(readers) == 0:
            return ''
        else:
            for r in readers:
                if str(r).upper().find('ACR122') > -1:
                    return r
            print 'Error seleccionando el lector. Cantidad de lectores: %s' % readers
            return ''

    def TransmitCommand(self, command):
        try:
            data, sw1, sw2 = self.connection.transmit(command, protocol=smartcard.CardConnection.CardConnection.T1_protocol)
            if sw1 != 0x90 or sw2 != 0x00:
                print 'sw1, sw2 = %02x %02x' % (sw1, sw2)
                print 'datos     = ' + smartcard.util.toHexString(data)
                return None
            else:
                return data
        except:
            pass

    def Connect(self,unidad):
        self.smartCardReader=self.getReader(unidad)
        self.connection = self.smartCardReader.createConnection()
        self.connection.connect()

    def Disconnect(self):
        self.connection.disconnect()

    def WaitForTag(self,cantidad):
        paso=0
        hallada=False
        while paso < cantidad:
            self.smartCardReader=self.getReader(paso)
            self.connection = self.smartCardReader.createConnection()
            
            tiempo_sin_tarjeta=time.time()

            while (time.time()- tiempo_sin_tarjeta < 1):
                try:
                    self.connection.connect()
                    hallada = True
                    tiempo_sin_tarjeta = tiempo_sin_tarjeta /2
                    paso=cantidad
                except:
                    hallada = False
                    pass
            paso = paso+1
            self.connection.disconnect()
        return hallada

    def Poll(self):
        data = self.TransmitCommand(smartcard.util.toBytes('FF00000004D44A0100'))
        if data != None and len(data)>=8:
            self.tag_number = data[2]
            self.target_number = data[3]
            self.sens_res = data[4:6]
            self.sel_res = data[6]
            self.uid_length = data[7]
            self.uid_value = data[8:]
            #print 'MIFARE tipo: ' + str(self.sel_res).strip()
            #print 'ID: ' + smartcard.util.toHexString(self.uid_value)
            return smartcard.util.toHexString(self.uid_value)
    
    def KeyA(self, block, key=DEFAULT_KEYA):
        APDU = smartcard.util.toBytes('FF000000')
        APDU.append(11 + self.uid_length)
        APDU += smartcard.util.toBytes('D440')
        APDU.append(self.target_number)
        APDU.append(0x60) # 0x61 for key B
        APDU.append(block)
        APDU += smartcard.util.toBytes(key)
        APDU += self.uid_value
        data = self.TransmitCommand(APDU)
        if data != None:
            if data[2] != 0:
                print 'Error:'
                print data
            return data[2]
        else:
            print 'Error:'
            return -1
            
    def PrepareKeyA(self, block, key):
        if self.KeyBlockNumber == None:
            self.KeyA(block, key)
            self.KeyBlockNumber = block
        elif self.KeyBlockNumber / 4 != block / 4:
            self.KeyA(block, key)
            self.KeyBlockNumber = block

    def ReadBlock(self, block, key=DEFAULT_KEYA):
        self.PrepareKeyA(block, key)
        APDU = smartcard.util.toBytes('FF00000005D440')
        APDU.append(self.target_number)
        APDU.append(0x30)
        APDU.append(block)
        data = self.TransmitCommand(APDU)
        if data != None:
            #print 'Bloque %02X: %s' % (block, smartcard.util.toHexString(data[3:]))
            return data[3:]
        else:
            return []
    
    def WriteBlock(self, block, values, key=DEFAULT_KEYA):
        self.PrepareKeyA(block, key)
        APDU = smartcard.util.toBytes('FF00000015D440')
        APDU.append(self.target_number)
        APDU.append(0xA0)
        APDU.append(block)
        APDU += values
        data = self.TransmitCommand(APDU)
        if data != None:
            if data[2] != 0:
                print 'Error:'
                print data
            return data[2]
        else:
            print 'Error:'
            return -1
    
    def ID(self,unidad):
        try:
            self.Connect(unidad)
            codigo=self.Poll()
            self.Disconnect()
            return codigo
        except:
            pass
            return None

    def Dump(self):
        self.Connect()

        data = []
        
        self.Poll()
        for block in range(1024 / 16): # MIFARE 1K
            data += self.ReadBlock(block)
        
        self.Disconnect()

        return data

    def DumpWritable(self):
        self.Connect()

        data = []
        
        self.Poll()
        for block in range(1, 1024 / 16): # MIFARE 1K
            if (block+1) % 4 != 0:
                data += self.ReadBlock(block)
        
        self.Disconnect()
        
        return data

    def WriteSequence(self, sequence, key=DEFAULT_KEYA):
        self.Connect()

        self.Poll()
        rest = sequence
        for block in range(1, 1024 / 16): # MIFARE 1K
            if (block+1) % 4 != 0:
                if len(rest) >= 16:
                    values = rest[0:16]
                    rest = rest[16:]
                else:
                    values = rest
                    rest = []
                    if len(values) > 0:
                        values += [0] * (16 - len(values))
                if len(values) > 0:
                    if (self.WriteBlock(block, values, key) == 0):
                        print 'OK escribiendo en bloque %02X ' % block
        
        self.Disconnect()
        
    def Wipe(self):
        self.WriteSequence([0] * (16 * (16 * 3 - 1)))
#        self.WriteSequence([i % 0x100 for i in range(16 * (16 * 3 - 1))])

def Usage(oParser):
    oParser.print_help()
    print
    print '  MIFARE RFID tag utilidad de lectura/escritura para el lector ACS ACR122'
    #print '  Source code put in the public domain by Didier Stevens, no Copyright'
    #print '  Use at your own risk'
    #print '  https://DidierStevens.com'
    return

def modo_escucha():
    control_usb=None
    try:
        control_usb= ControlUSB.ControlUSB()
        if (control_usb.p <> None):    
            readers = smartcard.System.readers()
            cantidadLectores=len(readers)
            print("Cantidad de lectores: "+str(cantidadLectores))
            licencia=Licencia.Licencia()
            if licencia.validar_licencia():
                while True:
                    revision=0
                    while revision < cantidadLectores:
                        #print("Anlizando lector: "+str(revision)) 
                        oMIFARE = cMIFARE(revision)
                        if oMIFARE.WaitForTag(cantidadLectores):
                            clave=oMIFARE.ID(revision)            
                            cedula=0
                            time.sleep(1)
                            if clave <> None:
                                print(clave+" en lector: "+str(revision)) 
                                consulta = 'SELECT cedula,nombres_propietario,validar_placa FROM propietarios where nfcid="' + str(clave) + '";'
                                valor, count_consulta, resultado= Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')                   
                                if valor == 1 and count_consulta>0:
                                    cedula,nombres_propietario,validar_placa=resultado.fetchone()
                                    cedula=str(cedula).split('.')[0]
                                    consulta = 'select count(*) from huellas_detectadas where cedula="'+str(cedula)+'" and fecha_entrada= CURDATE( ) AND MINUTE( TIMEDIFF( CURTIME( ) , hora_entrada ) ) <=5 and HOUR( TIMEDIFF( CURTIME( ) , hora_entrada ) ) =0 ;'
                                    valor, count_consulta, resultado= Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                                    
                                    if valor == 1 and count_consulta>0:
                                        cantidad=resultado.fetchone()[0]
                                        
                                        if cantidad ==0:
                                            consulta = 'insert into huellas_detectadas(cedula,fecha_entrada,hora_entrada,validar_placa) values("'+str(cedula)+'",CURDATE(),CURTIME(),'+str(validar_placa)+');'
                                            valor, count_consulta, resultado= Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')
                                            print('Se registro '+str(nombres_propietario))
                                            
                                            consulta = 'SELECT lectorpeatonalnfc FROM parqueadero;'
                                            valor, count_consulta, resultado= Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')                   
                                            if valor == 1 and count_consulta>0:
                                                lector_nfc_peatonal=resultado.fetchone()[0]                                                
                                                if int(lector_nfc_peatonal) == int(revision):
                                                    control_usb.send_signal("ABRE_PEATON")
                                                    print("Se abrio la puerta peatonal")
                                                    time.sleep(5)
                                                    control_usb.send_signal("CIERRA_PEATON")
                                        else: 
                                            consulta = 'SELECT lectorpeatonalnfc FROM parqueadero;'
                                            valor, count_consulta, resultado= Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')                   
                                            if valor == 1 and count_consulta>0:
                                                lector_nfc_peatonal=resultado.fetchone()[0]                                     
                                                if int(lector_nfc_peatonal) == int(revision):
                                                    control_usb.send_signal("ABRE_PEATON")
                                                    print("Se abrio la puerta peatonal")
                                                    time.sleep(5)
                                                    control_usb.send_signal("CIERRA_PEATON")
                                            
                        clave=None
                        revision=revision+1
        else:
            print 'No se detecto tarjeta de control'  
            exit()  
        
    except ValueError:
        print ("Error: "+str(ValueError))

def Principal(command):
    usageCommands = """\nComandos:
    id: display tag id
    dump: hexdump all tag blocks
    dumpwritable: hexdump all writable tag blocks
    wipe: overwrite all writable tag blocks with zeroes
    print: display all writable tag blocks
    read file: read all writable tag blocks and store in file
    write file: write content of file to all writable tag blocks
    shellcode: execute shellcode read from tag"""
   
    #command='id'
    if command == 'id':
        oMIFARE = cMIFARE()
        oMIFARE.WaitForTag()
        clave=oMIFARE.ID()
        return clave

    elif command == 'dump':
        oMIFARE = cMIFARE()
        oMIFARE.WaitForTag()
        oMIFARE.Dump()

    elif command == 'dumpwritable':
        oMIFARE = cMIFARE()
        oMIFARE.WaitForTag()
        oMIFARE.DumpWritable()

    elif command == 'wipe':
        oMIFARE = cMIFARE()
        oMIFARE.WaitForTag()
        oMIFARE.Dump()
        oMIFARE.Wipe()
        oMIFARE.DumpWritable()

    elif command == 'print':
        oMIFARE = cMIFARE()
        oMIFARE.WaitForTag()
        data = oMIFARE.DumpWritable()
        print ''.join([chr(i) for i in data])

    elif command == 'read':
        oMIFARE = cMIFARE()
        oMIFARE.WaitForTag()
        data = oMIFARE.DumpWritable()
        return ''.join([chr(i) for i in data])
        #WriteBinaryFile(filename, ''.join([chr(i) for i in data]))

    elif command == 'write':
        oMIFARE = cMIFARE()
        oMIFARE.WaitForTag()
        #oMIFARE.WriteSequence([ord(c) for c in ReadBinaryFile(filename)])
        oMIFARE.WriteSequence([ord(c) for c in 'john franklin ruiz neira;johnefe84@gmail.com;1984' ])
        oMIFARE.DumpWritable()
    else:
        print 'Opcion invalida'

#salida=Principal('id')
#print salida
modo_escucha()
#http://192.168.169.100:8080/
'''
#Se inicia el motor de voz
engine = pyttsx.init()
engine.setProperty('rate', 100)
#Se selecciona el idioma a utilizar
#voices = engine.getProperty('voices')
#for voice in voices:
#   print(voice.id)
#   engine.setProperty('voice', voice.id)
#engine.setProperty('voice', "spanish-latin-american")
#Se genera la voz a partir de un texto
engine.say('Hola! john franklin.')
engine.runAndWait()
'''