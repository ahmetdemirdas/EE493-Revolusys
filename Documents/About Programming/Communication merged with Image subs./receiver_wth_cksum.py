# This receiver only recognizes the ending indicator of the byte array
# The starting sequence should also be added
# It takes and displays the entire picture
# The picture should be divided

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import io
import serial
import time


def checksum(data, sum=0):
  """ Compute the Internet Checksum of the supplied data.  The checksum is
  initialized to zero.  Place the return value in the checksum field of a
  packet.  When the packet is received, check the checksum, by passing
  in the checksum field of the packet and the data.  If the result is zero,
  then the checksum has not detected an error.
  """
  # make 16 bit words out of every two adjacent 8 bit words in the packet
  # and add them up
  data = str(data)

  for i in range(0, len(data), 2):
    if i + 1 >= len(data):
      sum += ord(data[i]) & 0xFF
    else:
      w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i + 1]) & 0xFF)
      sum += w

  # take only 16 bits out of the 32 bit sum and add up the carries
  while (sum >> 16) > 0:
    sum = (sum & 0xFFFF) + (sum >> 16)

  # one's complement the result
  sum = ~sum

  return sum & 0xFFFF

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
    ser.write(bytes(request,encoding ='utf-8'))
    i = i + 1


  while ser.in_waiting:
    print("inside")
    action = ser.read(3) # read first three bytes to see if it is BYE or CHU
    action = action.decode('utf-8')
    x = ser.read_until('CHECK'.encode('utf-8')) #CKS
    check = ser.read_until('ENDOFLINE'.encode('utf-8'))
    check = bytearray(check)
    check = check[0:-9]
    print(type(check))
    check = int(check)
    x = bytearray(x)
    x = x[0:-5]
    checksum_result = checksum(data=x, sum=check)


    '''
    error correction should take place here
    '''
    print('the length of received data is ',len(x))
    print('the len of received_bytearray before concat:',len(received_bytearray))
    received_bytearray += bytearray(x)
    print('the length of received_bytearray after concat:',len(received_bytearray))
    if action == 'CHU': # if there will be other packets coming
      if checksum_result == 0:
        ser.write(bytes("NEXT",encoding = 'utf-8')) #if there is no error ask for the next byte, if there is error send the command 'AGAI' instead
      else:
        ser.write(bytes('AGAI', encoding='utf-8'))
    elif action == 'BYE': # if there will be no other chunks coming
      if checksum_result == 0:
        ser.write(bytes("NEXT",encoding = 'utf-8')) # this is to not to make transmitter be stuck in send_packet function after the transmission of last chunk (if no error)
      else:
        ser.write(bytes('AGAI', encoding='utf-8'))
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


