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
proc_img = np.array(np.zeros(img.shape))
print(img.shape[2])

hist_eql_img = np.array(np.zeros(img.shape))
for channel in range(img.shape[2]):
    ch_hist_eql = exposure.equalize_hist(img[:, :, channel])
    # hist_eql_img[:, :, channel] = ch_hist_eql
    hist_eql_img[:, :, channel] = exposure.rescale_intensity(
        ch_hist_eql, out_range=(0, 255))
hist_eql_img = hist_eql_img.astype(np.uint8)
print(type(img[1, 1, 1]))
print(type(hist_eql_img[1, 1, 1]))
# print(hist_eql_img)
# print(type(hist_eql_img))
# proc_img = IP.histogramEqualization(img)
# mod_proc_img = 255 * proc_img
# proc_img = IP.contrastStretch(img)
# print(mod_proc_img)
# Uncomment these lines if you want to see that the processed image looks fine.
# io.imshow(hist_eql_img)
# plt.title("hist eql img")
# plt.show()
# enc_img = cv2.imencode('.png', hist_eql_img)
# enc_img2 = encodeImage(enc_img[1])
# img_str = str(enc_img2)
# s2 = ast.literal_eval(img_str)
# dec_img = decodeImage(s2)
# print(dec_img)

# io.imshow(dec_img)
# print(dec_img)
# plt.title("Decoded Image")
# plt.show()
