from flask import Flask, jsonify, request
from ImageProcessor import ImageProcessor
import base64
import pickle
import numpy as np

app = Flask(__name__)


@app.route("/download", methods=["GET"])
def server_gui(processed_data):

    return


@app.route("/upload", methods=['POST'])
def gui_server():
    r = request.get_json()
    s1 = r.get("Images")
    s2 = r.get("Process")
    pro = ImageProcessor()
    processed_images = []
    if s2 == "Histogram Equalization":
        for x in range(len(s1)):
            nparr = np.frombuffer(base64.b64decode(s1[x]), np.uint8)
            processed_image = pro.histogramEqualization(nparr)
            processed_image_base64 = base64.b64encode(processed_image)
            base64_string = processed_image_base64.decode('ascii')
            processed_images.append(base64_string)
    elif s2 == "Contrast Stretching":
        for x in range(len(s1)):
            nparr = np.frombuffer(base64.b64decode(s1[x]), np.uint8)
            processed_image = pro.contrastStretch(nparr)
            processed_image_base64 = base64.b64encode(processed_image)
            base64_string = processed_image_base64.decode('ascii')
            processed_images.append(base64_string)
    elif s2 == "Log Compression":
        for x in range(len(s1)):
            nparr = np.frombuffer(base64.b64decode(s1[x]), np.uint8)
            processed_image = pro.logCompression(nparr)
            processed_image_base64 = base64.b64encode(processed_image)
            base64_string = processed_image_base64.decode('ascii')
            processed_images.append(base64_string)
    elif s2 == "Reverse Video":
        for x in range(len(s1)):
            nparr = np.frombuffer(base64.b64decode(s1[x]), np.uint8)
            processed_image = pro.reverseVideo(nparr)
            processed_image_base64 = base64.b64encode(processed_image)
            base64_string = processed_image_base64.decode('ascii')
            processed_images.append(base64_string)
    return "woo"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
