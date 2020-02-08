from PIL import Image
import numpy as np
im = Image.open('eee.png')
a = np.asarray(im)
print(a)
out = Image.fromarray(a)
out.show()

#Bu kod görüntüyü yüklüyor, dizilere ayırıyor ve bu dizilerden tekrar fotoğrafı oluşturuyor.