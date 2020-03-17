# The transmiteter sends the entire image with only end indicator
# The image should be divided
# Error correction should be employed
#Start indicator is necessary

from PIL import Image
import io
import serial
import time

ser = serial.Serial(
    port = '/dev/ttyS0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout =  100
)


im = Image.open(r"/home/pi/Desktop/serialcomm/schedule.JPG")  # resmi bytesIO object e donustur
buf = io.BytesIO()
im.save(buf, format = 'JPEG')
byte_im = buf.getvalue()
l = len(byte_im)
#print(byte_im)

i = 0
rec = io.BytesIO()
while 1:
    input1 = buf.getvalue()
    
    while i < 1:
        ser.write(input1)
        ser.write('ENDOFLINE'.encode('utf-8'))
        i = i + 1
        print("datasent")
    
        
#    if  ser.in_waiting:
 #       x = ser.readline()
  #      rec.write(x)
   #     im2 = Image.open(rec)
     #   im2.save(r"/home/pi/Desktop/serialcomm/savedim.jpeg")






#buf.seek(0) # bu niye var bilmiyorum ama kullanmislar
#im2 = Image.open(buf)
#im2.save(r"C:\Users\Eylul Atik\Desktop\dersler\bitirme\image3.jpeg")
#im2.show()