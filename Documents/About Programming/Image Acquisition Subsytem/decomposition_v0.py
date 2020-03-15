from PIL import Image
import os
import math
import sys
from io import BytesIO
import pickle

def long_slice(image_path, out_name, outdir, slice_size):
    img = Image.open(image_path)
    width, height = img.size
    upper = 0
    left = 0
    slices = int(math.ceil(height/slice_size))

    count = 1
    for slice in range(slices):
        #if we are at the end, set the lower bound to be the bottom of the image
        if count == slices:
            lower = height
        else:
            lower = int(count * slice_size)  

        bbox = (left, upper, width, lower)
        working_slice = img.crop(bbox)
        upper += slice_size
        #save the slice
        working_slice.save(os.path.join(outdir, "slice_" + out_name + "_" + str(count)+".jpg"))
        count +=1

if __name__ == '__main__':
    long_slice("test.jpg","test", os.getcwd(), 205)


count=1

while count<6:
    img = Image.open("slice_test_" + str(count) + ".jpg")
    if count==5:
        newImage = img.resize((1000, 204), Image.ANTIALIAS) 
    else:
        newImage = img.resize((1000, 205), Image.ANTIALIAS)         
    data_size=os.path.getsize("slice_test_" + str(count) + ".jpg")
    q=100
    while data_size>46080/5:
        q=q-1
        newImage.save("slice_test_new_" + str(count) + ".jpg", optimize=True, quality=q)
        data_size=os.path.getsize("slice_test_new_" + str(count) + ".jpg")
    count +=1

count = 1

while count<6:
    with open("slice_test_new_" + str(count)+".jpg", "rb") as image:
        f = image.read()
        b = bytearray(f)

    with open("data_" + str(count)+".dat", "wb") as t:
        pickle.dump(b, t)
    count +=1
