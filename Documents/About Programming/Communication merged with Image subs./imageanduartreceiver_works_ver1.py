# This receiver only recognizes the ending indicator of the byte array
# The starting sequence should also be added
# It takes and displays the entire picture
# The picture should be divided

from PIL import Image
#Image.LOAD_TRUNCATED_IMAGES = True
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
received_bytearray = bytearray()
i = 0
while 1:
  if i == 0:
    print('Send request')
    request = input(">> ")
    request = request + '\n'
    ser.write(bytes(request,encoding = 'utf-8'))
    i = i + 1
    

  while ser.in_waiting:
    print("inside")
    action = ser.read(3) # read first three bytes to see if it is BYE or CHU
    x = ser.read_until('ENDOFLINE'.encode('utf-8'))
    '''
    error correction should take place here
    '''
    received_bytearray = received_bytearray.append(x)
    if action == 'CHU': # if there will be other packets coming
      ser.write(bytes("NEXT",encoding = 'utf-8')) #if there is no error ask for the next byte, if there is error send the command 'AGAI' instead
    elif action == 'BYE': # if there will be no other chunks coming 
      ser.write(bytes("NEXT",encoding = 'utf-8')) # this is to not to make transmitter be stuck in send_packet function after the transmission of last chunk (if no error)
      if request == 'FIF\n': # if it was the last packet, then the photo is complete
        rec.write(received_bytearray)
        im2 = Image.open(rec)
        im2.save(r"/home/pi/Desktop/savedimage.jpeg")
        print("dataread")
      else:
        print('Send request')
        request = input(">> ")
        request = request + '\n'
        ser.write(bytes(request,encoding = 'utf-8'))



'''
    rec.write(x)
      
    im2 = Image.open(rec)
    im2.save(r"/home/pi/Desktop/savedimage.jpeg")
    print("dataread")
    i = 0 
'''