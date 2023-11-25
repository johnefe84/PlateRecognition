'''
Created on 3/12/2013

@author: johnefe
'''
import sys
import cv2
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPixmap, QStandardItemModel,QStandardItem

from Ventana import Ui_Ventana
import  MySQLdb._exceptions
import MySQLdb
import Licencia
import ControlUSB
import XMLConfig
import numpy as np
import hashlib
import time
import TTS
import Placas
import win32print #http://sourceforge.net/projects/pywin32/files/ win32 package
import win32ui #http://sourceforge.net/projects/pywin32/files/ win32 package
import win32con #http://sourceforge.net/projects/pywin32/files/ win32 package
import win32api
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab import rl_settings
import StringIO
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
import Consulta_BD
import qrcode
# class: gui pyqt4 ----------------------------

# const widget
NON = 9  # None
PRE = 10 # presentation
OPU = 11 # op user
VID = 12 #view all data

text0='L I C E N C I A  V A L I D A';
text1='L I C E N C I A   N O  V A L I D A';
text2='No se pudo detectar la placa';
text3='No se identificaron los caracteres';
text4='No se pudo delimitar la placa';
text5='Vehiculo registrado con exito';
text6='El vehiculo se identifico al salir con exito';   
text7='El visitante debe cancelar el parqueo';
text8='El propietario debe y no esta autorizado';
text9='El propietario no debe pero no esta autorizado';
text10='No hay datos del propietario/visitante';
text11='El vehiculo esta registrado y tiene propietario pero no hay datos del mismo';
text12='El vehiculo esta registrado pero no tiene asignado un propietario';
text13='El vehiculo no esta registrado';
text14='El visitante esta autorizado pero PARQUEADERO LLENO';
text15='El propietario esta autorizado pero PARQUEADERO LLENO';
text16='El vehiculo ya tiene registro de ingreso';
text17='El propietario/visitante no esta autorizado';
text18='El visitante no esta autorizado';
text19='PRECAUCION el vehiculo no tiene registro de ingreso';
text20='No se encontro la cedula del propietario a salir';
text21='No se encontro los datos del vehiculo a salir';
text22='PRECAUCION: El conductor del vehiculo no se ha identificado';
text23='ERROR: No se ha definido valor del minuto de parqueo' 
text24='ERROR: No se detecto imagen en '
# const user op
(INSERT, UPDATE, REMOVE) = (1000, 1001, 1002) 
 
class Gui(QtGui.QMainWindow):
    licencia=Licencia.Licencia()
    placas = Placas.Placas()
    
    def se_puede_reemplazar_msg(self,codigo,placa_nueva,camara):
        #actual=self.ui.mensajes.text();
        if (camara =='ENTRADA'):
            placa_actual=QtCore.QString(self.ui.resultado_e.text());
            color_actual=self.ui.e_semaforo_e.text(); 
            if (codigo != 2):
                #Significa que si hay una placa frente a la camara
                self.tiempo_sin_placa_e=time.time()
            else:
                #Si ha pasado 5 minutos sin detectar palca , entonces apaga el semaforo para
                #que no se caliente
                if (time.time()- self.tiempo_sin_placa_e > 300):
                    self.cambiar_semaforo('OFF','ENTRADA')
        elif (camara =='SALIDA'): 
            placa_actual=QtCore.QString(self.ui.resultado_s.text());
            color_actual=self.ui.e_semaforo_s.text(); 
            if (codigo != 2):
                #Significa que si hay una placa frente a la camara
                self.tiempo_sin_placa_s2=time.time()
            else:
                #Si ha pasado 5 minutos sin detectar palca , entonces apaga el semaforo para
                #que no se caliente
                if (time.time()- self.tiempo_sin_placa_s2 > 300):
                    self.cambiar_semaforo('OFF','SALIDA2')
        elif (camara =='ENTRADA2'):
            placa_actual=QtCore.QString(self.ui.resultado_e_2.text());
            color_actual=self.ui.e_semaforo_e_2.text(); 
            if (codigo != 2):
                #Significa que si hay una placa frente a la camara
                self.tiempo_sin_placa_e2=time.time()
            else:
                #Si ha pasado 5 minutos sin detectar palca , entonces apaga el semaforo para
                #que no se caliente
                if (time.time()- self.tiempo_sin_placa_e2 > 300):
                    self.cambiar_semaforo('OFF','ENTRADA2')
        elif (camara =='SALIDA2'): 
            placa_actual=QtCore.QString(self.ui.resultado_s_2.text());
            color_actual=self.ui.e_semaforo_s_2.text(); 
            if (codigo != 2):
                #Significa que si hay una placa frente a la camara
                self.tiempo_sin_placa_s=time.time()
            else:
                #Si ha pasado 5 minutos sin detectar palca , entonces apaga el semaforo para
                #que no se caliente
                if (time.time()- self.tiempo_sin_placa_s > 300):
                    self.cambiar_semaforo('OFF','SALIDA')    
              
        retorno = False;
        # 0 - 4 amarillo
        # 5 - 7 verde
        # 8 - 21 rojo
        if (codigo >= 0 and codigo <=4): 
            color_nuevo="AMARILLO";
        elif (codigo >= 5 and codigo <=7):
            color_nuevo='VERDE';    
        elif (codigo >= 8 and codigo <=24):
            color_nuevo="ROJO";
            
        # Si el codigo nuevo es verde y la placa nueva es diferente 
        # a la placa actual => remmplazo permitido
        if (placa_actual == QtCore.QString("??????")):
            retorno=True;
        else:
            if placa_nueva != QtCore.QString("??????"):
                #print('placa_actual'+placa_actual);
                #print('placa_nueva'+placa_nueva);
                if (placa_actual == QtCore.QString(placa_nueva)):
                    if (color_actual == 'AMARILLO'):
                        retorno=True;
                    elif (color_actual == 'VERDE'):
                        retorno=False;
                    elif (color_actual == 'ROJO'):
                        if (color_nuevo == 'VERDE'):
                            retorno=True;
                        else:    
                            if (color_nuevo == 'ROJO'):
                                if (codigo == 16 or codigo == 22 ):
                                    retorno=True;
                            else:    
                                retorno=False;
                    elif (color_actual == 'OFF'):
                        retorno=True;
                                    
                else:  
                    retorno=True;
            else:
                retorno=False;        
                 
        return retorno;
    
    def mostrar_mensaje(self,codigo,camara,nombres_propietario):
        if (codigo==0):
            fecha_expiracion=self.licencia.fecha_expiracion()
            self.ui.mensajes.setText(text0+'  -  V E N C E: '+fecha_expiracion);  
            return 'AMARILLO'
        elif (codigo==1):   
            fecha_expiracion=self.licencia.fecha_expiracion()
            self.ui.mensajes.setText(text1+'  -  V E N C I O: '+fecha_expiracion);
            return 'AMARILLO'
        elif (codigo==2):   
            self.ui.mensajes.setText(text2+' '+camara); 
            return 'AMARILLO'
        elif (codigo==3):   
            self.ui.mensajes.setText(text3+' '+camara); 
            return 'AMARILLO'
        elif (codigo==4):   
            self.ui.mensajes.setText(text4+' '+camara); 
            return 'AMARILLO'
        elif (codigo==5):   
            self.ui.mensajes.setText(text5+' '+camara+':'+str(nombres_propietario));    
            return 'VERDE'
        elif (codigo==6):   
            self.ui.mensajes.setText(text6+' '+camara+':'+str(nombres_propietario)); 
            return 'VERDE'
        elif (codigo==7):   
            self.ui.mensajes.setText(text7+' '+camara);
            return 'VERDE'
        elif (codigo==8):   
            self.ui.mensajes.setText(text8+' '+camara);
            return 'ROJO'
        elif (codigo==9):   
            self.ui.mensajes.setText(text9+' '+camara);
            return 'ROJO'
        elif (codigo==10):   
            self.ui.mensajes.setText(text10+' '+camara);
            return 'ROJO'
        elif (codigo==11):   
            self.ui.mensajes.setText(text11+' '+camara);
            return 'ROJO'
        elif (codigo==12):   
            self.ui.mensajes.setText(text12+' '+camara);
            return 'ROJO'
        elif (codigo==13):   
            self.ui.mensajes.setText(text13+' '+camara); 
            return 'ROJO'
        elif (codigo==14):   
            self.ui.mensajes.setText(text14+' '+camara);  
            return 'ROJO' 
        elif (codigo==15):   
            self.ui.mensajes.setText(text15+' '+camara);
            return 'ROJO'
        elif (codigo==16):   
            self.ui.mensajes.setText(text16+' '+camara); 
            return 'ROJO'
        elif (codigo==17):   
            self.ui.mensajes.setText(text17+' '+camara); 
            return 'ROJO'
        elif (codigo==18):   
            self.ui.mensajes.setText(text18+' '+camara); 
            return 'ROJO' 
        elif (codigo==19):   
            self.ui.mensajes.setText(text19+' '+camara); 
            return 'ROJO'
        elif (codigo==20):   
            self.ui.mensajes.setText(text20+' '+camara);
            return 'ROJO'
        elif (codigo==21):   
            self.ui.mensajes.setText(text21+' '+camara);  
            return 'ROJO'   
        elif (codigo==22):   
            self.ui.mensajes.setText(text22+' '+camara);  
            return 'ROJO'
        elif (codigo==23):   
            self.ui.mensajes.setText(text23+' '+camara);  
            return 'ROJO' 
        elif (codigo==24):   
            self.ui.mensajes.setText(text24+' '+camara);  
            return 'ROJO'                                                 
        else:   
            self.ui.mensajes.setText('Codigo sin texto asignado');       
            return 'AMARILLO'                 

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Ventana()
        self.ui.setupUi(self)
        self.ui.ingresar.clicked.connect(self.logeo_bd)   
        self.ui.registrar.setDisabled(True)
        self.ui.retirar.setDisabled(True)
        self.ui.registrar.clicked.connect(self.registrar_vehiculo)
        self.ui.retirar.clicked.connect(self.retirar_vehiculo) 
        self.ui.password.setEchoMode(QtGui.QLineEdit.Password)
        #self.ui.puerta_peaton.setDisabled(True)
        #self.ui.puerta_vehiculo.setDisabled(True)
         
        if self.licencia.validar_licencia():
            infile = open('ipservidor.txt', 'r')
            ipservidor=infile.read()
            db= MySQLdb.connect(ipservidor,'consulta','johnefe187471','parqueadero');
            infile.close()
            cursor = None   
            cursor = db.cursor()
              
            self._timer = QtCore.QTimer(self)
            self._timer.timeout.connect(self.play)
            self.mostrar_mensaje(0,'','')
            self.getParqueoActual()
            self.getParqueoHoy()
            self.cuposDIsponibles()
            command = 'SELECT vehiculo FROM servicio_parqueo where fecha_salida is null and hora_salida is null order by vehiculo asc;'
            #print (command)
            cursor.execute(command)
            db.close()
            #self.ui.listado_vehiculos.activated[str].connect(self.seleccionado)
            self.ui.listado_vehiculos.addItem("")
            if cursor.rowcount > 0:
                for renglon in range(0,cursor.rowcount): 
                    placa=cursor.fetchone()[0]
                    self.ui.listado_vehiculos.addItem(placa)
            try:
                TTS.hablar("Bienvenido"); 
            except:
                pass   
  
        else:   
            self.mostrar_mensaje(1,'','') 
              
        self.ui.logo.setPixmap(QPixmap("logo_baner.png")) 
        
    def generar_recibo(self,placa,hora_entrada,fecha_entrada,nombre,pagado,minutos,nombre_parqueadero,direccion_parqueadero,numero):
        imgPath2 = "codioqr.png"
        imgTemp = StringIO.StringIO()
        imgDoc = canvas.Canvas(imgTemp)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(numero)+";"+str(placa)+";"+str(fecha_entrada)+";"+str(hora_entrada)+";"+str(minutos)+";"+str(pagado))
        qr.make(fit=True)
        
        imgPath = qr.make_image() 
        imgPath.save(imgPath2,'png') 
        #imgDoc.drawImage(imgPath2, 2,2, 60,60)   
        #imgDoc.drawImage(imgPath3, 340,670, 262,84)  
        imgDoc.save()

        imgTemp = StringIO.StringIO()
        imgDoc = canvas.Canvas(imgTemp)
        imgPath3 = "logo_cliente.png"
        packet = StringIO.StringIO()
        ancho=10
        alto=8
        can = canvas.Canvas(packet, pagesize=(ancho*cm,alto*cm))
        consulta = 'SELECT nombre,direccion FROM parqueadero;'
        valor, count_consulta, resultado= Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')                   
        cantidad=0
        if valor == 1 and count_consulta>0:                                
            nombre_parqueadero,direccion_parqueadero=resultado.fetchone() 
        
        infile = open('ticket.txt', 'r')
    
        l1=infile.readline()
        l2=infile.readline()
        l3=infile.readline()
        l4=infile.readline()
        l5=infile.readline()
        l6=infile.readline()
        infile.close()
        can.setFont("Times-Roman", 7)
        #can.rotate(90)
        can.drawCentredString(4*cm,9.7*cm,"Software -PARA- Ideauto S.A.S. www.ideauto.co 3172333692 Bogota")
        can.setFont("Times-Roman", 18)
        can.drawCentredString(4*cm,8.75*cm, "Bienvenido")        
        can.setFont("Times-Roman", 9)
        can.drawCentredString(4*cm,8.3*cm, nombre_parqueadero)
        can.drawCentredString(4*cm,7.8*cm, direccion_parqueadero)
        can.drawCentredString(4*cm,7.3*cm, str(l1).strip())
        can.drawCentredString(4*cm,6.8*cm, str(l2).strip())
        can.drawCentredString(4*cm,6.3*cm, str(l3).strip())
        can.drawCentredString(4*cm,5.8*cm, str(l4).strip())
        can.drawCentredString(4*cm,5.3*cm, str(l5).strip())
        can.drawCentredString(4*cm,4.8*cm, str(l6).strip())
        can.setFont("Times-Roman", 16)
        can.drawCentredString(4*cm,4*cm, "Placa: "+str(placa).strip())
        
        can.setFont("Times-Roman", 9)
        can.drawString(0.8*cm,3.3*cm, "Fecha entrada: "+str(fecha_entrada))
        can.drawString(0.8*cm,2.8*cm, "Hora entrada: "+str(hora_entrada))
        can.drawString(0.8*cm,2.3*cm, "Fecha salida: "+time.strftime("%Y-%m-%d"))
        can.drawString(0.8*cm,1.8*cm, "Hora salida: "+ time.strftime("%H:%M:%S"))
        can.drawString(0.8*cm,1.3*cm, "Duracion: "+ str(minutos)+" minutos")
        can.drawString(0.8*cm,0.8*cm, "Valor pagado: $"+str(pagado))


        #vendido a,factura no, fecha emision,fecha vencimiento
        #can.roundRect(x,y,ancho,alto,radio,1,0)
        can.roundRect( 0.5*cm,0.5*cm,7*cm,9*cm,5,stroke=1, fill=0)
     
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet).getPage(0)
          
        imgDoc.drawImage(imgPath2, 130,20, 80,80)    
        #imgDoc.save()
        imgDoc.save()
        
        page = PdfFileReader(file("ticket_limpio_80x_100.pdf","rb")).getPage(0)
        overlay = PdfFileReader(StringIO.StringIO(imgTemp.getvalue())).getPage(0)
        page.mergePage(overlay)
        page.mergePage(new_pdf)
        
        output = PdfFileWriter()
        output.addPage(page)
        nombre_tiquete="tiquete_"+str(numero)+"_"+str(placa)+".pdf"
        output.write(file(nombre_tiquete,"w"))
        print('Se genero tiquete de pago con exito!!')
        fname= nombre_tiquete
        win32api.ShellExecute(0, "print", fname, None,  ".",  0)
        
    
    def registrar_vehiculo(self):
        placa_entrada=self.ui.placa_entrada.text()  
        usuario=self.ui.autorizado.text()
        visitantesinregistro=1
        foto=placa_entrada+'.jpg'
        resultado,apagar,mensaje,saludo_propietario,minutos_pagar=self.placas.insertarBaseDatos(placa_entrada,'insertar',usuario,foto,visitantesinregistro)  
        self.getParqueoActual()
        self.getParqueoHoy()
        self.cuposDIsponibles()
        
    def retirar_vehiculo(self):
        placa_salida=str(self.ui.listado_vehiculos.currentText())  
        usuario=self.ui.autorizado.text()
        visitantesinregistro=1
        foto=placa_salida+'.jpg'
        resultado,apagar,mensaje,saludo_propietario,minutos_pagar=self.placas.insertarBaseDatos(placa_salida,'retirar',usuario,foto,visitantesinregistro)  
        self.ui.a_pagar.setProperty("intValue", apagar)
        self.ui.minutos_pagar.setText(str(minutos_pagar))
        self.getParqueoActual()
        self.getParqueoHoy()
        self.cuposDIsponibles()
        consulta = 'SELECT fecha_ingreso,hora_ingreso,placavisitante,id_servicio FROM servicio_parqueo where propietario="99999999" and vehiculo="'+str(placa_salida)+'" and fecha_salida=curdate()'
        valor, count_consulta, resultado= Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')                   
        cantidad=0
        if valor == 1 and count_consulta>0:                                
            fecha_entrada,hora_entrada,placavisitante,id_servicio=resultado.fetchone() 
            
            consulta = 'SELECT nombre,direccion FROM parqueadero;'
            valor, count_consulta, resultado= Consulta_BD.realizar_consulta_base_datos('consulta','','',consulta,'','','')                   
            cantidad=0
            if valor == 1 and count_consulta>0:                                
                nombre_parqueadero,direccion_parqueadero=resultado.fetchone() 
            
            self.generar_recibo(placa_salida,hora_entrada,fecha_entrada,usuario[1],str(apagar),str(minutos_pagar),nombre_parqueadero,direccion_parqueadero,str(id_servicio))
                    
    def logeo_bd(self):
        try:
            infile = open('ipservidor.txt', 'r')
            ipservidor=infile.read()
            db= MySQLdb.connect(ipservidor,'consulta','johnefe187471','parqueadero');
            infile.close()    
            cursor = None   
            cursor = db.cursor()
            user_md5=hashlib.md5(str(self.ui.usuario.text())).hexdigest()
            password_md5=hashlib.md5(str(self.ui.password.text())).hexdigest()
            command = 'select idusuario,nombrecompleto from usuarios where usuario="' + user_md5 + '" and password="' + password_md5  + '";'
            #print (command)
            cursor.execute(command)
            db.close()
            if cursor.rowcount > 0:
                idusuario,nombre=cursor.fetchone()
                self.ui.registrar.setEnabled(True)
                self.ui.retirar.setEnabled(True)
                try:
                    print ('Logeo exitoso. Hola '+str(nombre)+".")
                    TTS.hablar("Hola. "+str(nombre))
                except:
                    pass
                self.ui.autorizado.setText(str(idusuario) + " | " + nombre)
                self.ui.ingresar.setDisabled(True)
                #self.ui.puerta_peaton.setDisabled(False)
                #self.ui.puerta_vehiculo.setDisabled(False)
                return True
            else:
                print ('User o password errado')
                try:
                    TTS.hablar("El usuario o la clave son incorrectos. Por favor verifique")
                except:
                    pass
                self.ui.autorizado.setText("CREDENCIALES DE ACCESO INCORRECTAS")
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowTitle("Error")
                i = QtGui.QIcon()
                i.addPixmap(QtGui.QPixmap("icono.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                msgBox.setWindowIcon(i)
                msgBox.setText('CREDENCIALES DE ACCESO INCORRECTAS')
                ret = msgBox.exec_();              
                return False    
        except ValueError:
            #self.ui.autorizado.setText("USUARIO O CONTRASENA INCORRECTA")
            return None
    
    def seleccionado(self,item):
        infile = open('ipservidor.txt', 'r')
        ipservidor=infile.read()
        db = MySQLdb.connect(ipservidor,'consulta','johnefe187471','parqueadero');   
        cursor = None   
        infile.close()
        cursor = db.cursor()
        cedula=str(self.ui.identificacion.text())
        command = "select piso,telefono from empresas where nombre='"+str(item)+"';"
        #print (command)
        cursor.execute(command)
        db.close()
        if cursor.rowcount > 0:
            piso,telefono=cursor.fetchone()
        self.ui.piso.setText(str(piso))
        self.ui.telefono.setText(str(telefono))
            
    def play(self):
        '''
        try: 
            #print(self.ui.autorizado.text())
            if self.ui.autorizado.text()<>"SIN AUTORIZACION DE ACCESO AL SISTEMA" and self.ui.autorizado.text()<>"CREDENCIALES DE ACCESO INCORRECTAS" :         
                self.update()
                self.getParqueoActual()
                self.cuposDIsponibles()    
        except TypeError:
            return None      
        '''        
        
    def cambiar_semaforo(self,color,camara):
        if (color=='ROJO'): 
            if (camara=='ENTRADA'):
                self.ui.semaforo_e.setPixmap(QPixmap("semaforo_rojo.png"));  
                self.ui.e_semaforo_e.setText("ROJO")
                self.control_usb.send_signal('SEME_ROJO')
            elif (camara=='ENTRADA2'):
                self.ui.semaforo_e_2.setPixmap(QPixmap("semaforo_rojo.png"));  
                self.ui.e_semaforo_e_2.setText("ROJO")
                self.control_usb.send_signal('SEME2_ROJO') 
            elif (camara=='SALIDA2'):
                self.ui.semaforo_s_2.setPixmap(QPixmap("semaforo_rojo.png"));  
                self.ui.e_semaforo_s_2.setText("ROJO")
                self.control_usb.send_signal('SEMS2_ROJO')        
            elif (camara=='SALIDA'): 
                self.ui.semaforo_s.setPixmap(QPixmap("semaforo_rojo.png"));   
                self.ui.e_semaforo_s.setText("ROJO")  
                self.control_usb.send_signal('SEMS_ROJO')
        elif (color == 'VERDE'): 
            if (camara=='ENTRADA'): 
                self.ui.semaforo_e.setPixmap(QPixmap("semaforo_verde.png"));
                self.ui.e_semaforo_e.setText("VERDE") 
                self.control_usb.send_signal('SEME_VERDE')
            elif (camara=='ENTRADA2'): 
                self.ui.semaforo_e_2.setPixmap(QPixmap("semaforo_verde.png"));
                self.ui.e_semaforo_e_2.setText("VERDE") 
                self.control_usb.send_signal('SEME2_VERDE')   
            elif (camara=='SALIDA'):     
                self.ui.semaforo_s.setPixmap(QPixmap("semaforo_verde.png"));
                self.ui.e_semaforo_s.setText("VERDE")
                self.control_usb.send_signal('SEMS_VERDE') 
            elif (camara=='SALIDA2'):   
                self.ui.semaforo_s_2.setPixmap(QPixmap("semaforo_verde.png"));
                self.ui.e_semaforo_s_2.setText("VERDE")
                self.control_usb.send_signal('SEMS2_VERDE')     
        elif (color == 'AMARILLO'):   
            if (camara=='ENTRADA'):
                self.ui.semaforo_e.setPixmap(QPixmap("semaforo_amarillo.png"));
                self.ui.e_semaforo_e.setText("AMARILLO") 
                self.control_usb.send_signal('SEME_AMARILLO')
            elif (camara=='ENTRADA2'):     
                self.ui.semaforo_e_2.setPixmap(QPixmap("semaforo_amarillo.png"));
                self.ui.e_semaforo_e_2.setText("AMARILLO") 
                self.control_usb.send_signal('SEME_AMARILLO')
            elif (camara=='SALIDA'): 
                self.ui.semaforo_s.setPixmap(QPixmap("semaforo_amarillo.png")); 
                self.ui.e_semaforo_s.setText("AMARILLO")  
                self.control_usb.send_signal('SEMS_AMARILLO')     
            elif (camara=='SALIDA2'): 
                self.ui.semaforo_s_2.setPixmap(QPixmap("semaforo_amarillo.png")); 
                self.ui.e_semaforo_s_2.setText("AMARILLO")  
                self.control_usb.send_signal('SEMS2_AMARILLO') 
        elif (color == 'OFF'): 
            if (camara=='ENTRADA'):
                self.ui.semaforo_e.setPixmap(QPixmap("semaforo_off.png"));
                self.ui.e_semaforo_e.setText("OFF") 
                self.control_usb.send_signal('SEME_OFF')
            elif (camara=='ENTRADA2'):     
                self.ui.semaforo_e_2.setPixmap(QPixmap("semaforo_off.png"));
                self.ui.e_semaforo_e_2.setText("OFF") 
                self.control_usb.send_signal('SEME_OFF')
            elif (camara=='SALIDA'): 
                self.ui.semaforo_s.setPixmap(QPixmap("semaforo_off.png")); 
                self.ui.e_semaforo_s.setText("OFF")  
                self.control_usb.send_signal('SEMS_OFF')     
            elif (camara=='SALIDA2'): 
                self.ui.semaforo_s_2.setPixmap(QPixmap("semaforo_off.png")); 
                self.ui.e_semaforo_s_2.setText("AMARILLO")  
                self.control_usb.send_signal('SEMS2_OFF')  
            
    def cuposDIsponibles(self):
        try:
            infile = open('ipservidor.txt', 'r')
            ipservidor=infile.read()
            db= MySQLdb.connect(ipservidor,'consulta','johnefe187471','parqueadero')
            infile.close()    
            cursor = None   
            cursor = db.cursor()
            command = 'select nombre,propietarios,visitantes from cupos_disponibles;'   
            cursor.execute(command)
            db.close()
            modelo = QStandardItemModel (1, 2)
            for fila in range(cursor.rowcount):
                parqueadero,cuposp,cuposv = cursor.fetchone()  
                self.ui.visitantes.setText(str(cuposv))
                self.ui.parqueadero.setText(str(parqueadero))
            cursor.close()
            del cursor
            
        except MySQLdb._exceptions.ProgrammingError as ex_q:
            #self.showMessage(str(ex_q), 'ERROR')
            return None
    def getParqueoHoy(self):
        try:
            infile = open('ipservidor.txt', 'r')
            ipservidor=infile.read()
            db= MySQLdb.connect(ipservidor,'consulta','johnefe187471','parqueadero')
            infile.close()    
            cursor = None   
            cursor = db.cursor()
            command = 'select vehiculo,fecha_ingreso,hora_ingreso,fecha_salida,hora_salida,valor_cancelado from servicio_parqueo where fecha_ingreso is not null and fecha_Salida is not null;'
            cursor.execute(command)
            db.close()
            # get data 
            #data = []
            columnas = 3
            modelo = QStandardItemModel (cursor.rowcount,columnas)
            #self.ui.tabla.setHorizontalHeader(0,"PLACA")
            if cursor.rowcount >0:
                for fila in range(cursor.rowcount):
                    vehiculo,fechai,horai,fechas,horas,valor = cursor.fetchone()  
                    item1 = QStandardItem(vehiculo)
                    item2 = QStandardItem(fechai.strftime('%m/%d/%Y'))
                    item3 = QStandardItem(str(horai))
                    item4 = QStandardItem(fechas.strftime('%m/%d/%Y'))
                    item5 = QStandardItem(str(horas))
                    item6 = QStandardItem(str(valor))
                    modelo.setItem(fila, 0, item1)
                    modelo.setItem(fila, 1, item2)
                    modelo.setItem(fila, 2, item3)
                    modelo.setItem(fila, 3, item4)
                    modelo.setItem(fila, 4, item5)
                    modelo.setItem(fila, 5, item6)
                    modelo.setHorizontalHeaderLabels(["PLACA","FECHA ENTRADA","HORA ENTRADA","FECHA SALIDA","HORA SALIDA","CANCELADO"])
                self.ui.parqueo_hoy.setModel(modelo)
                self.ui.parqueo_hoy.resizeColumnsToContents()
            elif (cursor.rowcount ==0):
                item1 = QStandardItem("")
                item2 = QStandardItem("")
                item3 = QStandardItem("")
                item4 = QStandardItem("")
                item5 = QStandardItem("")
                item6 = QStandardItem("")
                modelo.setItem(0, 0, item1)
                modelo.setItem(0, 1, item2)
                modelo.setItem(0, 2, item3)
                modelo.setItem(0, 3, item4)
                modelo.setItem(0, 4, item5)
                modelo.setItem(0, 5, item6)
                modelo.setHorizontalHeaderLabels(["PLACA","PROPIETARIO","FECHA ENTRADA","HORA ENTRADA","VISITANTE"])
                self.ui.parqueo_hoy.setModel(modelo)
                self.ui.parqueo_hoy.resizeColumnsToContents()
            cursor.close()
            del cursor
            db= MySQLdb.connect(ipservidor,'consulta','johnefe187471','parqueadero')
            infile.close()    
            cursor = None   
            cursor = db.cursor()
            command = 'select sum(valor_cancelado) from servicio_parqueo where fecha_ingreso is not null and fecha_Salida is not null;'
            cursor.execute(command)
            db.close()
            if cursor.rowcount >0:
                total_dia = cursor.fetchone()[0] 
                self.ui.total_dia.setText(str(total_dia))


        except MySQLdb._exceptions.ProgrammingError as ex_q:
            self.showMessage(str(ex_q), 'ERROR')
            return None
            
    def getParqueoActual(self):
        try:
            infile = open('ipservidor.txt', 'r')
            ipservidor=infile.read()
            db= MySQLdb.connect(ipservidor,'consulta','johnefe187471','parqueadero')
            infile.close()    
            cursor = None   
            cursor = db.cursor()
            command = 'select cupos_visitantes from parqueadero;'
            cursor.execute(command)

            if cursor.rowcount >0:
                cupos_visitantes=cursor.fetchone()[0] 
            
            cursor = None   
            cursor = db.cursor()
            command = 'select id_servicio,vehiculo,propietario,fecha_ingreso,hora_ingreso from servicio_parqueo where fecha_salida is null and hora_salida is null;'
            cursor.execute(command)
            db.close()
                         
            # get data 
            #data = []
            columnas = 3
            modelo = QStandardItemModel (cupos_visitantes,columnas)
            #self.ui.tabla.setHorizontalHeader(0,"PLACA")
            if cursor.rowcount >0:
                for fila in range(cursor.rowcount):
                    id_servicio,placa,propietario,fechai,horai = cursor.fetchone()  
                    item1 = QStandardItem(str(id_servicio))
                    item2 = QStandardItem(placa)
                    item3 = QStandardItem(str(propietario))
                    item4 = QStandardItem(fechai.strftime('%m/%d/%Y'))
                    item5 = QStandardItem(str(horai))
                    modelo.setItem(fila, 0, item1)
                    modelo.setItem(fila, 1, item2)
                    modelo.setItem(fila, 2, item3)
                    modelo.setItem(fila, 3, item4)
                    modelo.setItem(fila, 4, item5)
                    modelo.setHorizontalHeaderLabels(["ID","PLACA","PROPIETARIO","FECHA ENTRADA","HORA ENTRADA"])
                self.ui.parqueo_actual.setModel(modelo)
                self.ui.parqueo_actual.resizeColumnsToContents()
            elif (cursor.rowcount ==0):
                item1 = QStandardItem("")
                item2 = QStandardItem("")
                item3 = QStandardItem("")
                item4 = QStandardItem("")
                item5 = QStandardItem("")
                modelo.setItem(0, 0, item1)
                modelo.setItem(0, 1, item2)
                modelo.setItem(0, 2, item3)
                modelo.setItem(0, 3, item4)
                modelo.setItem(0, 4, item5)
                modelo.setHorizontalHeaderLabels(["ID","PLACA","PROPIETARIO","FECHA ENTRADA","HORA ENTRADA"])
                self.ui.parqueo_actual.setModel(modelo)
                self.ui.parqueo_actual.resizeColumnsToContents()
            cursor.close()
            del cursor

        except MySQLdb._exceptions.ProgrammingError as ex_q:
            self.showMessage(str(ex_q), 'ERROR')
            return None

def convertir_hora(a):
    b = a.split(':')
    return int(b[0]) * 3600 + int(b[1]) * 60 + int(b[2])  
    
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()