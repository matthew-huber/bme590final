from ImageProcessor import ImageProcessor
from skimage import io, exposure
from matplotlib import pyplot as plt
import cv2
from image_processor_gui import decodeImage
from image_processor_server import encodeImage
import numpy as np
import ast

IP = ImageProcessor()
img = io.imread("TestImages/color_img.jpg")

# proc_img = IP.histogramEqualization(img)
# proc_img = IP.contrastStretch(img)
proc_img = IP.logCompression(img)
print(proc_img)
print("seperator")
enc_img = cv2.imencode('.png', proc_img)
dec_img = decodeImage(enc_img[1])
dec_img.setflags(write=1)
if img.ndim >= 3:
    temp = np.zeros(img.shape, dtype='uint8')
    temp = np.copy(dec_img[:, :, 0])
    dec_img[:, :, 0] = dec_img[:, :, 2]
    dec_img[:, :, 2] = temp
print(dec_img)

io.imshow(dec_img)
# print(dec_img)
# plt.title("Decoded Image")
plt.show()
