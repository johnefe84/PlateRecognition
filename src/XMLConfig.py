'''
Created on 22/08/2014

@author: johnefe
'''

from xml.dom import minidom

class XMLConfig:
    
    came_tipo=''
    came_dir=''
    cams_tipo=''
    cams_dir=''  
        
    def leer_datos(self):      
        xmldoc = minidom.parse('config.xml')     
        camaras=xmldoc.getElementsByTagName('camara')
        
        for node in camaras:  # visit every node <bar />
            conf_name=node.getAttribute('name')
            
            alist=node.getElementsByTagName('tipo')
            for a in alist:
                tipo= a.childNodes[0].nodeValue
                if (conf_name == 'entrada'):
                    came_tipo = tipo
                else:
                    cams_tipo = tipo    
                    #print tipo
            
            alist=node.getElementsByTagName('direccion')
            for a in alist:
                direccion = a.childNodes[0].nodeValue
                if (conf_name == 'entrada'):
                    came_dir = direccion
                else:
                    cams_dir = direccion
                    #print direccion
                    
        return str(came_tipo),str(came_dir),str(cams_tipo),str(cams_dir)    
                