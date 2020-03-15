import sys
from PIL import Image
from io import BytesIO
import pickle
import numpy as np
import os

count=1
while count<6:
    with open("data_"+str(count)+".pickle", "rb") as f:
        b = pickle.load(f)
    stream = BytesIO(b)
    image = Image.open(stream).convert("RGB")
    stream.close()
    image.save("reconstructed_"+str(count)+".jpg")
    count+=1

s_1 = np.asarray(Image.open("reconstructed_1.jpg"))
s_2 = np.asarray(Image.open("reconstructed_2.jpg"))
s_3 = np.asarray(Image.open("reconstructed_3.jpg"))
s_4 = np.asarray(Image.open("reconstructed_4.jpg"))
s_5 = np.asarray(Image.open("reconstructed_5.jpg"))

os.remove("reconstructed_1.jpg")
os.remove("reconstructed_2.jpg")
os.remove("reconstructed_3.jpg")
os.remove("reconstructed_4.jpg")
os.remove("reconstructed_5.jpg")

imnew=np.concatenate((s_1,s_2,s_3,s_4,s_5))
out = Image.fromarray(imnew)


out.save("reconstructed_image.jpg")
out.show()	