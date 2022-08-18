import numpy as np

import cv2

from matplotlib import pyplot as plt

image = cv2.imread('projectpro_noise_20.jpg',1)

image_bw = cv2.imread('projectpro_noise_20.jpg',0)

noiseless_image_bw = cv2.fastNlMeansDenoising(image_bw, None, 20, 7, 21)

noiseless_image_colored = cv2.fastNlMeansDenoisingColored(image,None,20,20,7,21)

#Displays image inside a window
cv2.imshow('Original Image(colored)',image)
cv2.imshow('Image after removing the noise (colored)', noiseless_image_colored)
cv2.imshow('Original Image (grayscale)', image_bw)
cv2.imshow('Image after removing the noise (grayscale)', noiseless_image_bw)
# Waits for a keystroke
cv2.waitKey(0)
# Destroys all the windows created
cv2.destroyAllwindows()