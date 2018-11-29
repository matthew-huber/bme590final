from flask import Flask, jsonify, request
from ImageProcessor import ImageProcessor
import base64

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
            processed_image = pro.histogramEqualization(
                base64.b64decode(s1[x]))
            processed_image_base64 = base64.b64encode(processed_image)
            base64_string = processed_image_base64.decode('ascii')
            processed_images.append(base64_string)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
