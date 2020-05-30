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
import random
import numpy
import matplotlib.pyplot as plt

def sensor_real_distance(intended_distance, sd_type):
    real_distance_values = [3, 5, 7, 10, 15, 20, 30, 50, 100, 150] # cm
    measured_distance_mean = [3.80, 4.87, 6.82, 10.33, 16.60, 20.39, 29.56, 49.08, 97.68, 147.49] # cm
    constant_sd = 0.1 # Constant standard deviation can be arraged here.
    exp_sd = [0.04, 0.05, 0.05, 0.22, 0.12, 0.07, 0.13, 0.11, 0.41, 0.41]
    if sd_type == "constant":
        measured_sd = constant_sd * numpy.ones(len(real_distance_values))
    elif sd_type == "experimental":
        measured_sd = exp_sd
    mean_fit = numpy.polyfit(real_distance_values, measured_distance_mean, 5)
    sd_fit = numpy.polyfit(real_distance_values, measured_sd, 5)
    distance_function = numpy.poly1d(mean_fit)
    sd_function = numpy.poly1d(sd_fit)
    real_distance = random.normalvariate(distance_function(intended_distance), sd_function(intended_distance))
    # The following 12 lines are written to observe the behaviour of the fitted functions in usage range. Optimum
    # fitting degree is found as 5.
    # mean = numpy.zeros(1501)
    # sd = numpy.zeros(1501)
    # for i in range(1501):
    #     mean[i] =distance_function(i/10)
    #     sd[i] =sd_function(i/10)
    # x_axis = numpy.linspace(0, 150, num=1501)
    # plt.figure()
    # plt.plot(x_axis, mean, "-")
    # plt.savefig("mean_sensor.png")
    # plt.figure()
    # plt.plot(x_axis, sd, "-")
    # plt.savefig("sd_sensor.png")
    return real_distance


def communication_error_rate(environment, real_distance, sd_type):
    real_distance_values = [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 30, 45] # cm
    measured_error_rate_mean_light = [0, 1.04, 1.11, 1.22, 1.32, 1.82, 2.17, 2.54, 2.93, 3.32, 3.69, 4.13, 6.13, 8.78,
                                      19.77] # percentage
    measured_error_rate_mean_dark = [0, 1.02, 1.10, 1.22, 1.33, 1.79, 1.63, 2.02, 2.44, 2.88, 3.62, 4.01, 5.11, 6.54,
                                     12.06] # percentage
    constant_sd = 0.01 # Constant standard deviation can be arranged here.
    exp_sd_light = []  # I couldn't find related data yet.
    exp_sd_dark = []  # I couldn't find related data yet.
    if sd_type == "constant":
        measured_sd = constant_sd * numpy.ones(len(real_distance_values))
    elif sd_type == "experimental":
        if environment == "light":
            measured_sd = exp_sd_light
        elif environment == "dark":
            measured_sd = exp_sd_light
    if environment == "light":
        measured_error_rate_mean = measured_error_rate_mean_light
    elif environment == "dark":
        measured_error_rate_mean = measured_error_rate_mean_dark
    mean_fit = numpy.polyfit(real_distance_values, measured_error_rate_mean, 3)
    sd_fit = numpy.polyfit(real_distance_values, measured_sd, 3)
    error_function = numpy.poly1d(mean_fit/100) # normalizing percentage
    sd_function = numpy.poly1d(sd_fit)
    error_rate = random.normalvariate(error_function(real_distance), sd_function(real_distance))
    # # The following 12 lines are written to observe the behaviour of the fitted functions in usage range. Optimum
    # # fitting degree is found as 3.
    # mean = numpy.zeros(451)
    # sd = numpy.zeros(451)
    # for i in range(451):
    #     mean[i] =error_function(i/10)
    #     sd[i] =sd_function(i/10)
    # x_axis = numpy.linspace(0, 45, num=451)
    # plt.figure()
    # plt.plot(x_axis, mean, "-")
    # plt.savefig("mean_comm.png")
    # plt.show()
    # plt.figure()
    # plt.plot(x_axis, sd, "-")
    # plt.savefig("sd_comm.png")
    return error_rate

def communication_error_creator_concentrated(packet_byte_data, error_rate):
    byte_data_mutable = bytearray(packet_byte_data)
    mess_ratio=0.8 # Described how much the wrong byte is randomized.
    number_of_bytes=len(packet_byte_data)
    prob_1=random.random()
    if prob_1<error_rate:
        for i in range(number_of_bytes):
            prob = random.random()
            if prob < mess_ratio:
                byte_data_mutable[i] = random.randint(0, 255)
    packet_byte_data = bytes(byte_data_mutable)
    return packet_byte_data




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
    check = int(check)
    print('check is', check)
    x = bytearray(x)
    x = x[0:-5]
    
    x = communication_error_creator_concentrated(x,0.7)
    x = bytes(x)
    control_check = checksum(x)
    print('contorl check', control_check)
    print('lenght of x',len(x))
    checksum_result = checksum(data=x, sum=check)
    print('checksumresult is ', checksum_result)


    '''
    error correction should take place here
    '''
    '''
    print('the length of received data is ',len(x))
    print('the len of received_bytearray before concat:',len(received_bytearray))
    received_bytearray += bytearray(x)
    print('the length of received_bytearray after concat:',len(received_bytearray))
    '''
    if action == 'CHU': # if there will be other packets coming
      if checksum_result == 0:
        print('the length of received data is ',len(x))
        print('the len of received_bytearray before concat:',len(received_bytearray))
        received_bytearray += bytearray(x)
        print('the length of received_bytearray after concat:',len(received_bytearray))
        ser.write(bytes("NEXT",encoding = 'utf-8')) #if there is no error ask for the next byte, if there is error send the command 'AGAI' instead
      else:
        print('ERROR DETECTED')  
        ser.write(bytes('AGAI', encoding='utf-8'))
    elif action == 'BYE': # if there will be no other chunks coming
      if checksum_result == 0:
        print('the length of received data is ',len(x))
        print('the len of received_bytearray before concat:',len(received_bytearray))
        received_bytearray += bytearray(x)
        print('the length of received_bytearray after concat:',len(received_bytearray))
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
            
      else:
        print('ERROR DETECTED')
        ser.write(bytes("SPEC", encoding='utf-8'))
        '''
      if request == 'FIF\n': # if it was the last packet, then the photo is complete
        rec.write(received_bytearray)
        im2 = Image.open(rec)
        im2.save(r"/home/pi/Desktop/savedimage.jpeg")
        print("dataread")
      else:
        print('Send request')
        request = input(">> ")
        request = request + '\n'
        '''
        