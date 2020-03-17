# This receiver only recognizes the ending indicator of the byte array
# The starting sequence should also be added
# It takes and displays the entire picture
# The picture should be divided

from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True
import io
import serial
import time

ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=100
)

rec = io.BytesIO()
while 1:
    while ser.in_waiting:
        print("inside")
        x = ser.read_until('ENDOFLINE'.encode('utf-8'))
        rec.write(x)
        
        im2 = Image.open(rec)
        im2.save(r"/home/pi/Desktop/savedimage.jpeg")
        print("dataread")
