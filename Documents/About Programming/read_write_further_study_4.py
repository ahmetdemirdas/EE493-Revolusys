# 	load and display an image with Matplotlib
from matplotlib import image
from matplotlib import pyplot
import numpy as np
import os
from PIL import Image

i=0
y= np.zeros((256,256,3))

image = image.imread('eee.jpg')

while i<3:
	x = image[:,:,i]
	np.savetxt(os.path.join("text_" + str(i)+".html"), x, fmt='%s')
	i=i+1

i=0

while i<3:
	y[:,:,i] = np.loadtxt(os.path.join("text_" + str(i)+".html"), dtype=np.object) 
	i=i+1

y = y.astype(np.uint8)

img = Image.fromarray(y)
img.save('test.jpg')