#!/usr/bin/env python3

# The transmiteter sends the entire image with only end indicator
# The image should be divided --> image is divided into 5 and 1 kB packet sending is employed
# Error correction should be employed
#Start indicator is necessary --> receiver request is employed


from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL import Image
import io
import serial
import time
import os

def send_one_kB(serialobj,packet,count): # this function sends 1 kB chunk of a given packet
    
    if(len(packet) < 1024): # if the lenght of the packet is smaller than 1 kB send all of it and tell the car to go with BYE command
        serialobj.write('BYE'.encode('utf-8'))
        serialobj.write(packet)
        serialobj.write('ENDOFLINE'.encode('utf-8')) # receiver reads until it sees ENDOFLINE
        return 0
    else:   #if its length is bigger than 1 kB send it as chunks of 1 kB
        if (count+1)*1024 < len(packet): #as long as we dont reach at the end of the packet execute this
            serialobj.write('CHU'.encode('utf-8')) # CHU implies there will be at least one more chunk after this one 
            serialobj.write(packet[count*1024:(count+1)*1024])
            serialobj.write('ENDOFLINE'.encode('utf-8'))
            return 1
        else: # when the loop condition becomes false, send the last chunk
            serialobj.write('BYE'.encode('utf-8')) #BYE means this is the last chunk and that the car can go after receiving it.
            serialobj.write(packet[count*1024:])
            serialobj.write('ENDOFLINE'.encode('utf-8'))
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
            elif action == 'AGAI':
                pass
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
                with open(original_file, 'wb') as f_output:
                    f_output.write(file_bytes.read())
                break





ser = serial.Serial(    # declare serial port object
   port = '/dev/ttyS0',
   baudrate = 115200,
   parity = serial.PARITY_NONE,
   stopbits = serial.STOPBITS_ONE,
   bytesize = serial.EIGHTBITS,
   timeout =  100
)


im = Image.open(r"/home/pi/Desktop/3muskEEters.png")  # resmi bytesIO object e donustur
im.save(r"/home/pi/Desktop/3muskEEters.jpg", format = 'JPEG')
im.close()
im2 = Image.open(r"/home/pi/Desktop/3muskEEters.jpg")
print(im2.size)
q=10
data_size=os.path.getsize(r"/home/pi/Desktop/3muskEEters.jpg")

while data_size>46080:              # reduce the data size approximately to 45 kB
    q=q-1
    im2.save(r"/home/pi/Desktop/3muskEEters.jpg", optimize=True, quality=q)
    data_size=os.path.getsize(r"/home/pi/Desktop/3muskEEters.jpg")
im2.close()
im3 = Image.open(r"/home/pi/Desktop/3muskEEters.jpg")
buf = io.BytesIO()
im3.save(buf, format = 'JPEG')
im3.close()


all_bytes = buf.getvalue()        # Slice the image into five big packets
l = len(all_bytes)
rec = io.BytesIO()
rec.write(all_bytes)
im4 = Image.open(rec)
im4.save(r"/home/pi/Desktop/savedimage.jpg")
rec_size= os.path.getsize(r"/home/pi/Desktop/savedimage.jpg")


slicelen = round(l/5)
first = all_bytes[0:slicelen]
second = all_bytes[slicelen:2*slicelen]
third = all_bytes[2*slicelen:3*slicelen]
fourth = all_bytes[3*slicelen:4*slicelen]
fifth = all_bytes[4*slicelen:]


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


