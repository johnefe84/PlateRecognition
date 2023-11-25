'''
Created on 21/06/2014

@author: johnefe
'''
"""
Create certificates and private keys for the 'simple' example.
"""

from certgen import *   

cakey = createKeyPair(TYPE_RSA, 1024)
careq = createCertRequest(cakey, CN='IDEAUTO SAS',C='CO',ST='CUNDINAMARCA',L='BOGOTA',O='900770454',emailAddress='info@ideauto.co')
cacert = createCertificate(careq, (careq, cakey), 0, (0, 60*60*24*365*68)) # 68 annos
cacert = createCertificate(careq, (careq, cakey), 0, (0, 60*60*24*365*68)) # 68 annos
open('certs/CA.key', 'w').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, cakey))
open('certs/CA.lic', 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cacert))
    