from PIL import Image
import os

img = Image.open("eee.jpg")
newImage = img.resize((256, 256), Image.ANTIALIAS)         
data_size=os.path.getsize("eee_new.jpg")
q=100
while data_size>51200/5:
    q=q-1
    newImage.save("eee_new.jpg", optimize=True, quality=q)
    data_size=os.path.getsize("eee_new.jpg")
    print(os.path.getsize("eee_new.jpg"))
