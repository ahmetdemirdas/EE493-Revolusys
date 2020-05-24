# Import functions
from sensor_read_value import sensor_real_distance
from comm_error_rate import communication_error_rate
from comm_error_creator import communication_error_creator_homogeneous, communication_error_creator_concentrated, \
    erroneus_packet_selector
# Import necessary libraries
from PIL import ImageFile
from PIL import Image
import io
import numpy

ImageFile.LOAD_TRUNCATED_IMAGES = True


# Here, I will create the compressed byte file to illustrate functions.
def compress(original_file, max_size, scale):
    assert (0.0 < scale < 1.0)
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


all_bytes = compress("layout.jpg", 46080, 0.8)
# Let's start using functions.
intended_stopping_distance = 10  # cm
real_stopping_distance = sensor_real_distance(intended_stopping_distance, "experimental")
communication_error_rate = communication_error_rate("light", real_stopping_distance, "constant")
print("communication error rate (percentage) = "+str(numpy.round(communication_error_rate*100,1)))
all_bytes_1 = communication_error_creator_homogeneous(all_bytes, communication_error_rate)
number_of_packets = 1
current_packet_index = 0  # 1 packet, current packet index is 0, so our concentrated error creator function will
# certainly be activated.
wrong_byte_indexes = erroneus_packet_selector(number_of_packets, communication_error_rate)
all_bytes_2 = communication_error_creator_concentrated(all_bytes, wrong_byte_indexes, current_packet_index)
# Compare the followings and see the difference
print(all_bytes)
print(all_bytes_1)
print(all_bytes_2)
