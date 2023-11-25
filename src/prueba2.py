'''
Created on 24/10/2013

@author: johnefe
'''

import urllib2
import time
import logging

print "Recording video..."
response = urllib2.urlopen("http://192.168.0.10:8080")
filename = time.strftime("%Y%m%d%H%M%S",time.localtime())+".avi"
f = open(filename, 'wb')

video_file_size_start = 0
video_file_size_end = 1048576 * 20  # end in 20 mb
block_size = 1024

while True:
    try:
        buffer = response.read(block_size)
        if not buffer:
            break
        video_file_size_start += len(buffer)
        if video_file_size_start > video_file_size_end:
            break
        f.write(buffer)

    except Exception, e:
        logging.exception(e)
f.close()
