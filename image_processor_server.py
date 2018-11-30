from flask import Flask, jsonify, request
from ImageProcessor import ImageProcessor
import base64
import time
import io
import matplotlib.image as mpimg

app = Flask(__name__)


@app.route("/download", methods=["GET"])
def server_gui(processed_data):
    return_data = {
        "OG Images": s1,
        "Timestamps": s3,
        "OG Height": OG_height,
        "OG Width": OG_width,
        "Processed Images": processed_image,
        "Time Spent": time1,
        "Processed Height": processed_height,
        "Processed Width": processed_width,
    }
    return return_data


@app.route("/upload", methods=['POST'])
def gui_server():
    r = request.get_json()
    global s1
    global s3
    s1 = r.get("Images")
    s2 = r.get("Process")
    s3 = r.get("Timestamps")
    check = data_validation(r)
    if check:
        pro = ImageProcessor()
        global processed_image
        global processed_height
        global processed_width
        global OG_height
        global OG_width
        processed_images = []
        processed_height = []
        processed_width = []
        OG_height = []
        OG_width = []
        if s2 == "Histogram Equalization":
            start = time.time()
            for x in range(len(s1)):
                byte_image = base64.b64decode(s1[x])
                image_buf = io.BytesIO(byte_image)
                i = mpimg.imread(image_buf, format='JPG')
                i_shape = i.shape
                OG_height.append(i_shape[0])
                OG_width.append(i_shape[1])
                processed_image = pro.histogramEqualization(i)
                processed_shape = processed_image.shape
                processed_height.append(processed_shape[0])
                processed_width.append(processed_shape[1])
                processed_image_base64 = base64.b64encode(processed_image)
                base64_string = processed_image_base64.decode('ascii')
                processed_images.append(base64_string)
            end = time.time()
        elif s2 == "Contrast Stretching":
            start = time.time()
            for x in range(len(s1)):
                byte_image = base64.b64decode(s1[x])
                image_buf = io.BytesIO(byte_image)
                i = mpimg.imread(image_buf, format='JPG')
                i_shape = i.shape
                OG_height.append(i_shape[0])
                OG_width.append(i_shape[1])
                processed_image = pro.contrastStretch(i)
                processed_shape = processed_image.shape
                processed_height.append(processed_shape[0])
                processed_width.append(processed_shape[1])
                processed_image_base64 = base64.b64encode(processed_image)
                base64_string = processed_image_base64.decode('ascii')
                processed_images.append(base64_string)
            end = time.time()
        elif s2 == "Log Compression":
            start = time.time()
            for x in range(len(s1)):
                byte_image = base64.b64decode(s1[x])
                image_buf = io.BytesIO(byte_image)
                i = mpimg.imread(image_buf, format='JPG')
                i_shape = i.shape
                OG_height.append(i_shape[0])
                OG_width.append(i_shape[1])
                processed_image = pro.logCompression(i)
                processed_shape = processed_image.shape
                processed_height.append(processed_shape[0])
                processed_width.append(processed_shape[1])
                processed_image_base64 = base64.b64encode(processed_image)
                base64_string = processed_image_base64.decode('ascii')
                processed_images.append(base64_string)
            end = time.time()
        elif s2 == "Reverse Video":
            start = time.time()
            for x in range(len(s1)):
                byte_image = base64.b64decode(s1[x])
                image_buf = io.BytesIO(byte_image)
                i = mpimg.imread(image_buf, format='JPG')
                i_shape = i.shape
                OG_height.append(i_shape[0])
                OG_width.append(i_shape[1])
                processed_image = pro.reverseVideo(i)
                processed_shape = processed_image.shape
                processed_height.append(processed_shape[0])
                processed_width.append(processed_shape[1])
                processed_image_base64 = base64.b64encode(processed_image)
                base64_string = processed_image_base64.decode('ascii')
                processed_images.append(base64_string)
            end = time.time()
        global time1
        time1 = end - start
        return "woo"
    return "Bad Data send new Image(s) or Modified Version of Image"

def data_validation(dict):
    s1 = dict.get("Images")
    s2 = dict.get("Process")
    s3 = dict.get("Timestamps")
    if s1 is not None and s2 is not None and s3 is not None:
        return True
    return False

if __name__ == "__main__":
    app.run(host="0.0.0.0")
