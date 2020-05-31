#!/usr/bin/env python3

# This is the complete transmitter code.

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL import Image
import io
import serial
import time
import os



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
            w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i+1]) & 0xFF)
            sum += w

    # take only 16 bits out of the 32 bit sum and add up the carries
    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)

    # one's complement the result
    sum = ~sum

    return sum & 0xFFFF


def send_one_kB(serialobj, packet, count): # this function sends 1 kB chunk of a given packet

    
    if(len(packet) < 1024): # if the lenght of the packet is smaller than 1 kB send all of it and tell the car to go with BYE command
        check = checksum(packet)
        print('Check result of the taken 1 kB data: ', check)
        check = str(check)
        serialobj.write('BYE'.encode('utf-8'))
        serialobj.write(packet)
        serialobj.write('CHECK'.encode('utf-8'))
        serialobj.write(check.encode('utf-8'))
        serialobj.write('ENDOFLINE'.encode('utf-8')) # receiver reads until it sees ENDOFLINE
        print('The count is equal to',count, ' and packet length is smaller than 1kB')
        print('Packet length is',len(packet))
        return 0
    else:   #if its length is bigger than 1 kB send it as chunks of 1 kB
        if (count+1)*1024 < len(packet): #as long as we dont reach at the end of the packet execute this
            packet_to_send = packet[count * 1024:(count + 1) * 1024]
            check = checksum(packet_to_send)
            print('Check result of the taken 1 kB data: ', check)
            check = str(check)
            serialobj.write('CHU'.encode('utf-8')) # CHU implies there will be at least one more chunk after this one
            serialobj.write(packet_to_send)
            serialobj.write('CHECK'.encode('utf-8'))
            serialobj.write(check.encode('utf-8'))
            serialobj.write('ENDOFLINE'.encode('utf-8'))
            print('The count is equal to', count, ' and CHU')
            print('Packet length is', len(packet[count*1024:(count+1)*1024]))
            return 1
        else: # when the loop condition becomes false, send the last chunk
            packet_to_send = packet[count*1024:]
            check = checksum(packet_to_send)
            print('Check result of the taken 1 kB data: ', check)
            check = str(check)
            serialobj.write('BYE'.encode('utf-8')) #BYE means this is the last chunk and that the car can go after receiving it.
            serialobj.write(packet_to_send)
            serialobj.write('CHECK'.encode('utf-8'))
            serialobj.write(check.encode('utf-8'))
            serialobj.write('ENDOFLINE'.encode('utf-8'))
            print('The count is equal to',count,' and BYE')
            print('Packet length is',len(packet[count*1024:]))
            return 0

def send_packet(serialobj,packet):  # this function takes the serial port and a packet and transmits it
    condition = 1
    count = 0
    while condition:
        condition = send_one_kB(serialobj,packet,count)
        while serialobj.in_waiting == 0:
            pass
        if serialobj.in_waiting > 0:
            action = serialobj.read(4)
            action = action.decode('utf-8')
            if action == 'NEXT':
                count = count + 1
                print('next received')
            elif action == 'AGAI':
                print('agai received')
            elif action == 'SPEC':
                print('spec received')
                condition = 1
            else:
                print("ERROR REQUEST NOT DEFINED")

def compress(original_file, max_size, scale):
    assert(0.0 < scale < 1.0)
    orig_image = Image.open(original_file)
    cur_size = orig_image.size

    while True:
        cur_size = (int(cur_size[0] * scale), int(cur_size[1] * scale))
        resized_file = orig_image.resize(cur_size, Image.ANTIALIAS)

        with io.BytesIO() as file_bytes:
            resized_file.save(file_bytes, optimize=True, quality=95, format='jpeg')
            if file_bytes.tell() <= max_size:
                file_bytes.seek(0, 0)
                byte = file_bytes.getvalue()
                break
    return byte




ser = serial.Serial(    # declare serial port object
   port = '/dev/ttyS0',
   baudrate = 115200,
   parity = serial.PARITY_NONE,
   stopbits = serial.STOPBITS_ONE,
   bytesize = serial.EIGHTBITS,
   timeout =  100
)


all_bytes = compress(r"/home/pi/Desktop/3muskEEters.jpg", 46080, 0.8)

       # Slice the image into five big packets
l = len(all_bytes)
rec = io.BytesIO()
rec.write(all_bytes)
im4 = Image.open(rec)
im4.save(r"/home/pi/Desktop/savedimage.jpg")
rec_size= os.path.getsize(r"/home/pi/Desktop/savedimage.jpg")


slicelen = round(l/5)
first = all_bytes[0:slicelen]
fir_len = len(first)
second = all_bytes[slicelen:2*slicelen]
sec_len = len(second)
third = all_bytes[2*slicelen:3*slicelen]
thi_len = len(third)
fourth = all_bytes[3*slicelen:4*slicelen]
fou_len = len(fourth)
fifth = all_bytes[4*slicelen:]
fif_len = len(fifth)



while 1:   # the main loop


    while ser.in_waiting == 0:   # run in this empty loop if there is no request
        pass

    request = ser.read(4)
    request = request.decode('utf-8')
    print(request)

    if request == 'FIR\n':                # Deciding which packet to send based on the request
        send_packet(ser,first)
        print("firstsent")
    elif request == 'SEC\n':
        send_packet(ser,second)
        print("secondsent")
    elif request == 'THI\n':
        send_packet(ser,third)
        print("thirdsent")
    elif request == 'FOU\n':
        send_packet(ser,fourth)
        print("fourthsent")
    elif request == 'FIF\n':
        send_packet(ser,fifth)
        print("fifthsent")
    else:
        pass