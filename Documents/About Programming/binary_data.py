
with open("eee.jpg", 'rb') as imageFile:
    string = imageFile.read()

with open("message.txt", 'wb')  as outfile:  
  outfile.write(string)  # Write your data

print(string)

with open("message.txt", 'rb')  as inputfile:
    imagetext = inputfile.read()

with open("out.jpg",'wb') as imagenew:
    imagenew.write(imagetext)
