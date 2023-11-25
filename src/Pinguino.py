'''
Created on 2/09/2014

@author: johnefe
'''
#-------------------------------------------------------------------------------
# Pinguino Class by Marin Purgar (marin.purgar@gmail.com)
#-------------------------------------------------------------------------------
import usb
import sys

class Pinguino():

    VENDOR = 0x04D8
    PRODUCT = 0xFEAA
    CONFIGURATION = 0x01 # if bootloader v4.x
    #CONFIGURATION = 0x03 # if bootloader v2.x
    #print type(CONFIGURATION)
    INTERFACE = 0
    ENDPOINT_IN = 0x81 # if bootloader v4.x
    #ENDPOINT_IN = 0x82 # if bootloader v2.x
    ENDPOINT_OUT = 0x01

    device = None
    handle = None

    def __init__(self,):
        for bus in usb.busses():
            #print usb.busses()
            for dev in bus.devices:
                if dev.idVendor == self.VENDOR and dev.idProduct == self.PRODUCT:
                    self.device = dev
                    print "vendor",dev.idVendor
                    print "idproduct",dev.idProduct
        return None

    def pinguinoOpen(self):
        if not self.device:
            print >> sys.stderr, "Unable to find device!"
            return None
        try:
            self.handle = self.device.open()
            self.handle.setConfiguration(self.CONFIGURATION)
            self.handle.claimInterface(self.INTERFACE)
        except usb.USBError, err:
            print >> sys.stderr, err
            self.handle = None
        return self.handle

    def pinguinoClose(self):
        try:
            self.handle.releaseInterface()
        except Exception, err:
            print >> sys.stderr, err
        self.handle, self.device = None, None

    def pinguinoRead(self, length, timeout = 0):
        return self.handle.bulkRead(self.ENDPOINT_IN, length, timeout)

    def pinguinoWrite(self, buffer, timeout = 0):
        return self.handle.bulkWrite(self.ENDPOINT_OUT, buffer, timeout)
    
pinguino = Pinguino()
if pinguino.pinguinoOpen() == None:
    print "No se pudo abrir Pinguino!"
    pinguino.pinguinoClose() # Cerrar aplicacion de manera correcta.
else:
    print "Se encontro pinguino"
    pinguino.pinguinoWrite("A", 0)    