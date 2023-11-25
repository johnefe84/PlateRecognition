'''
Created on 28/07/2014

@author: johnefe
'''
#import parallel
#import time
from pynguino import PynguinoUSB 

class ControlUSB:
	
	p=None
	
	def __init__(self):
		if (self.p == None):
			try:
				self.p=PynguinoUSB("v2")
			except:
				pass
	
	def send_signal(self,signal):
		try:
			#p = parallel.Parallel()
			#time.sleep(2)
			#Primer semaforo
			if   (signal == 'SEME_VERDE'):   
				self.p.write("Abc")  
				#p.setData(1)#verde
			elif (signal == 'SEME_AMARILLO'):
				self.p.write("abC")    
				#p.setData(2)#amarillo
			elif (signal == 'SEME_ROJO'):
				self.p.write("aBc") 
			elif (signal == 'SEME_OFF'):
				self.p.write("abc")	    
				#p.setData(3)#rojo
			#Segundo semaforo	
			elif (signal == 'SEMS_VERDE'): 
				self.p.write("Def") 
				#p.setData(4)
			elif (signal == 'SEMS_AMARILLO'):
				self.p.write("deF")  
				#p.setData(5)
			elif (signal == 'SEMS_ROJO'): 
				self.p.write("dEf") 
			elif (signal == 'SEMS_OFF'):
				self.p.write("def")		
			#Tercer semaforo	
			elif (signal == 'SEME2_VERDE'):   
				self.p.write("Abc")  
				#p.setData(1)#verde
			elif (signal == 'SEME2_AMARILLO'):
				self.p.write("abC")    
				#p.setData(2)#amarillo
			elif (signal == 'SEME2_ROJO'):
				self.p.write("aBc")  
			elif (signal == 'SEME2_OFF'):
				self.p.write("abc")	   
				#p.setData(3)#rojo
			#Cuarto semaforo	
			elif (signal == 'SEMS2_VERDE'): 
				self.p.write("Def") 
				#p.setData(4)
			elif (signal == 'SEMS2_AMARILLO'):
				self.p.write("deF")  
				#p.setData(5)
			elif (signal == 'SEMS2_ROJO'): 
				self.p.write("dEf") 	
				#p.setData(6)  
			elif (signal == 'SEMS2_OFF'):
				self.p.write("def")		                   
			elif (signal == 'RESET'): 
				self.p.write("r") 
				#p.setData(0)
			else:       
				self.p.write("r") 
				#p.setData(0)	
		except :
			#print("Error de acceso al puerto paralelo")
			pass
