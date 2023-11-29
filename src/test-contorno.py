import numpy as np 
import cv2

image = cv2.imread('/Users/john.ruiz/placa1.jpg')
orig_image = image.copy()
cv2.imshow('Original Image', orig_image)

# Grayscale and Binarize
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,100,255,cv2.THRESH_OTSU) 

# Find Contours
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through each contour
#for c in contours:
#    x,y,w,h = cv2.boundingRect(c)
#    cv2.rectangle(orig_image, (x, y), (x+w, y+h), (255, 0, 255), 2)
#    cv2.imshow('Bounding Rectangle', orig_image)
cv2.waitKey(0)
cv2.destroyAllWindows()