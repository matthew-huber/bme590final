from ImageProcessor import ImageProcessor
from skimage import io
from matplotlib import pyplot as plt
import cv2
from image_processor_gui import decodeImage

IP = ImageProcessor()
img = io.imread("TestImages/color_img.jpg")

proc_img = IP.histogramEqualization(img)
mod_proc_img = 255 * proc_img
# proc_img = IP.contrastStretch(img)
print(mod_proc_img)
# Uncomment these lines if you want to see that the processed image looks fine.
# io.imshow(proc_img)
# plt.show()
enc_img = cv2.imencode('.png', mod_proc_img)

dec_img = decodeImage(enc_img[1])
print(dec_img)

io.imshow(dec_img)
plt.show()
