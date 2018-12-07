from flask import Flask, jsonify, request
from ImageProcessor import ImageProcessor
import base64
import time
import io
import matplotlib.image as mpimg
from img_db import DB_Image_Meta
import json
import cv2


app = Flask(__name__)


@app.route("/get_images/<user>", methods=["GET"])
def get_images(user):
    image_list = []
    for image in DB_Image_Meta.objects.raw({"user": user}):
        image_list.append(image.img_file_path)
    return jsonify(image_list)


@app.route("/processing_type/<filename>", methods=["GET"])
def processing_type(filename):
    image_data = {}
    for image in DB_Image_Meta.objects.raw({"_id": filename}):
        image_data["process_done"] = image.processing_types[-1]
    return jsonify(image_data)


@app.route("/image_data/<filename>", methods=["GET"])
def get_image_data(filename):
    image_data = {}
    for image in DB_Image_Meta.objects.raw({"_id": filename}):
        image_data["process_done"] = image.processing_types[-1]
        upload_date = image.upload_timestamp
        upload_date = upload_date.strftime("%Y-%m-%d %H:%M:%S")
        image_data["date_upload"] = upload_date
        image_data["process_times"] = image.processing_times[-1]
        px = str(image.processed_width[-1]) + " x "
        px = px + str(image.processed_height[-1])
        image_data["image_pixels"] = px
    return jsonify(image_data)


@app.route("/delete_image/<filename>", methods=["GET"])
def delete_image(filename):
    DB_Image_Meta.objects.raw({"_id": filename}).delete()

    return jsonify({"status": "true"})


@app.route("/download", methods=["GET"])
def server_gui():
    return_data = {
        "OG Images": str(IMAGES),
        "Timestamps": str(TIMESTAMPS),
        "OG Height": str(OG_height),
        "OG Width": str(OG_width),
        "Processed Images": str(processed_images),
        "Time Spent": str(processing_times),
        "Processed Height": str(processed_height),
        "Processed Width": str(processed_width),
    }
    r = json.dumps(return_data)

    return r


@app.route("/user_list", methods=["GET"])
def user_list():
    list_of_users = []
    for image in DB_Image_Meta.objects.all():
        if image.user not in list_of_users:
            list_of_users.append(image.user)
    return jsonify(list_of_users)


@app.route("/upload", methods=['POST'])
def gui_server():
    r = request.get_json()
    global IMAGES
    global PROCESSING_TYPE
    global TIMESTAMPS
    global FILENAMES
    global USERNAME
    IMAGES = r.get("Images")
    PROCESSING_TYPE = r.get("Process")
    TIMESTAMPS = r.get("Timestamps")
    FILENAMES = r.get("FileNames")
    USERNAME = r.get("User")

    check = data_validation(r)

    pro = ImageProcessor()
    global processed_images
    global processed_height
    global processed_width
    global OG_height
    global OG_width
    global processing_times
    processing_times = []
    processed_images = []
    processed_height = []
    processed_width = []
    OG_height = []
    OG_width = []

    if check:
        for x in range(len(IMAGES)):

            byte_image = base64.b64decode(IMAGES[x])
            i = decodeImage(byte_image)

            start = time.time()
            processed_image = process(i, PROCESSING_TYPE, pro)
            enc_image = cv2.imencode('.jpg', processed_image)
            end = time.time()

            proc_time = end-start
            proc_time = float("{0:.4f}".format(proc_time))

            processing_times.append(proc_time)

            OG_characteristics = getImageCharacteristics(i)
            addImageCharacteristics(OG_characteristics, "original")
            proc_characteristics = getImageCharacteristics(processed_image)
            addImageCharacteristics(proc_characteristics, "processed")

            encoded_proc_img = encodeImage(enc_image[1])
            processed_images.append(encoded_proc_img)

        addImagesToDatabase()
        return "woo"
    return "Bad Data send new Image(s) or Modified Version of Image"


def data_validation(dict):
    s1 = dict.get("Images")
    s2 = dict.get("Process")
    s3 = dict.get("Timestamps")
    if s1 is not None and s2 is not None and s3 is not None:
        return True
    return False


def addImagesToDatabase():
    """adds image metadata to the database

    :return: None
    """
    for x in range(len(IMAGES)):
        file_path = FILENAMES[x]
        user = USERNAME
        processing_time = processing_times[x]
        processing_type = PROCESSING_TYPE
        original_height = OG_height[x]
        original_width = OG_width[x]
        proc_height = processed_height[x]
        proc_width = processed_width[x]
        upload_timestamp = TIMESTAMPS[0]

        query_set = DB_Image_Meta.objects.raw({"_id": file_path})
        if query_set.count() > 0:
            db_img = DB_Image_Meta.objects.raw({"_id": file_path}).first()

        else:
            db_img = DB_Image_Meta(img_file_path=file_path,
                                   user=user,
                                   original_height=original_height,
                                   original_width=original_width,
                                   upload_timestamp=upload_timestamp)

        db_img.processing_times.append(processing_time)
        db_img.processing_types.append(processing_type)
        db_img.processed_height.append(proc_height)
        db_img.processed_width.append(proc_width)

        db_img.save()


def process(img, proc_type, IP):
    """Applies specified proc_type to img using the ImageProcessor IP

    :param img:
    :param proc_type:
    :param IP:
    :return:
    """
    if proc_type == "Histogram Equalization":
        proc_img_buf = IP.histogramEqualization(img)
        proc_img = proc_img_buf
    elif proc_type == "Contrast Stretching":
        proc_img = IP.contrastStretch(img)
    elif proc_type == "Reverse Video":
        proc_img = IP.reverseVideo(img)
    elif proc_type == "Log Compression":
        proc_img = IP.logCompression(img)

    return proc_img


def getImageCharacteristics(img):
    """Gets the height and width characteristics of an image

    :param img:
    :return:
    """
    img_char = {}
    img_char["height"] = img.shape[0]
    img_char["width"] = img.shape[1]

    return img_char


def addImageCharacteristics(img_char, img_type):
    """Adds the image characteristics (made from getImageCharacteristics
    function) to the global image characteristic variables

    :param img_char:
    :param img_type:
    :return:
    """
    if img_type == "original":
        OG_height.append(img_char["height"])
        OG_width.append(img_char["width"])
    elif img_type == "processed":
        processed_height.append(img_char["height"])
        processed_width.append(img_char["width"])


def decodeImage(byte_img):
    """Decodes a byte_image to a numpy array

    :param byte_img:
    :return:
    """
    image_buf = io.BytesIO(byte_img)

    i = mpimg.imread(image_buf, format='JPG')

    return i


def encodeImage(img):
    """Encodes a numpy array into a byte image

    :param img:
    :return:
    """
    bytes_img = img.tobytes()
    processed_image_base64 = base64.b64encode(bytes_img)
    base64_string = processed_image_base64.decode('ascii')
    return base64_string


if __name__ == "__main__":
    app.run(host="0.0.0.0")
