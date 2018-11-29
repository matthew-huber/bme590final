from flask import Flask, jsonify, request
from ImageProcessor import ImageProcessor
import base64
import pickle
import numpy as np
import time

app = Flask(__name__)


@app.route("/download", methods=["GET"])
def server_gui(processed_data):
    return_data = {
        "OG Images": s1,
        "Timestamps": s3,
        "OG Height": s4,
        "OG Width": s5,
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
    global s4
    global s5
    s1 = r.get("Images")
    s2 = r.get("Process")
    s3 = r.get("Timestamps")
    s4 = r.get("OG Height")
    s5 = r.get("OG Width")
    pro = ImageProcessor()
    global processed_image
    global processed_height
    global processed_width
    processed_images = []
    processed_height = []
    processed_width = []
    if s2 == "Histogram Equalization":
        start = time.time()
        for x in range(len(s1)):
            nparr = np.frombuffer(base64.b64decode(s1[x]), np.uint8)
            print(nparr.shape)
            processed_image = pro.histogramEqualization(nparr)
            print(processed_image.shape)
            height, width, channels = processed_image.shape
            processed_height.append(height)
            processed_width.append(width)
            processed_image_base64 = base64.b64encode(processed_image)
            base64_string = processed_image_base64.decode('ascii')
            processed_images.append(base64_string)
        end = time.time()
    elif s2 == "Contrast Stretching":
        start = time.time()
        for x in range(len(s1)):
            nparr = np.frombuffer(base64.b64decode(s1[x]), np.uint8)
            processed_image = pro.contrastStretch(nparr)
            height, width, channels = processed_image.shape
            processed_height.append(height)
            processed_width.append(width)
            processed_image_base64 = base64.b64encode(processed_image)
            base64_string = processed_image_base64.decode('ascii')
            processed_images.append(base64_string)
        end = time.time()
    elif s2 == "Log Compression":
        start = time.time()
        for x in range(len(s1)):
            nparr = np.frombuffer(base64.b64decode(s1[x]), np.uint8)
            processed_image = pro.logCompression(nparr)
            height, width, channels = processed_image.shape
            processed_height.append(height)
            processed_width.append(width)
            processed_image_base64 = base64.b64encode(processed_image)
            base64_string = processed_image_base64.decode('ascii')
            processed_images.append(base64_string)
        end = time.time()
    elif s2 == "Reverse Video":
        start = time.time()
        for x in range(len(s1)):
            nparr = np.frombuffer(base64.b64decode(s1[x]), np.uint8)
            processed_image = pro.reverseVideo(nparr)
            height, width, channels = processed_image.shape
            processed_height.append(height)
            processed_width.append(width)
            processed_image_base64 = base64.b64encode(processed_image)
            base64_string = processed_image_base64.decode('ascii')
            processed_images.append(base64_string)
        end = time.time()
    global time1
    time1 = end - start
    return "woo"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
