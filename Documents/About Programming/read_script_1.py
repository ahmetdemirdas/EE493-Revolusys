# Python program to read 
# image using PIL module 
  
# importing PIL 
from PIL import Image 
  
# Read image 
img = Image.open('eee.png') 
  
# Output Images 
#img.show() 
  
# prints format of image 
#print(img.format) 
  
# prints mode of image 
#print(img.mode) 

a=list(img.getdata())
#out = Image.fromarray(a)
#out.show()

#Son kısım çalışmadı ama bu kod ilginizi çekebilir. Basit bir görüntü yükleme kodu.
#Çalışmama sebebi "Image.fromarray"'in "list" değil "array" tipi dosyalarla çalışması. 