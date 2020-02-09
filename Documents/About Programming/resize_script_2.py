from PIL import Image

img = Image.open("eee.png")
newImage = img.resize((1024, 768), Image.ANTIALIAS)         

newImage.save("C:\Users\onura\Desktop", optimize=True, quality=95)

newImage.show() 