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
    """
        Performs a query of the database based on
        username. This returns all image file names
        asscoiated that user. sent back to gui
    :param user: string that contains name of the user
    :return: list with filepaths/names of all images
    associated that user
    """
    image_list = []
    for image in DB_Image_Meta.objects.raw({"user": user}):
        image_list.append(image.img_file_path)
    return jsonify(image_list)


@app.route("/processing_type/<filename>", methods=["GET"])
def processing_type(filename):
    """
        Performs a query for a unique file and pulls what
        type of image processing has last been done on it
    :param filename: the file or image being searched for
    :return: dict with only the type of image processing
        that has been last performed
    """
    image_data = {}
    for image in DB_Image_Meta.objects.raw({"_id": filename}):
        image_data["process_done"] = image.processing_types[-1]
    return jsonify(image_data)


@app.route("/image_data/<filename>", methods=["GET"])
def get_image_data(filename):
    """
        Performs a query for a unique file and pulls all
        image meta data from the stored file. Sends this back
        to the gui for display
    :param filename: the file or image being searched for
    :return: dictornary with all image meta data
    """
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
    """
        Performs a query for a unique file and then uses
        the mongo command delete to remove this unique file
    :param filename: unique filepath/name stored in the database
    :return: returns the boolean true to confirm deletion
    """
    DB_Image_Meta.objects.raw({"_id": filename}).delete()

    return jsonify({"status": "true"})


@app.route("/user_list", methods=["GET"])
def user_list():
    """
        Queries the database for all users stored in it.
        Then sends a list of these users back to the gui.
    :return: JSON list of users
    """
    list_of_users = []
    for image in DB_Image_Meta.objects.all():
        if image.user not in list_of_users:
            list_of_users.append(image.user)
    return jsonify(list_of_users)


@app.route("/upload", methods=['POST'])
def gui_server():
    """
        Post request that receives data from the gui.
        In this same function the data is unpacked,
        processed, repackaged and sent back to the
        gui. This is all done in a modular function
    :return: JSON if the data from the gui is correct
    . If the data is incorrect than a string is returned.
    """
    r = request.get_json()
    IMAGES = r.get("Images")
    PROCESSING_TYPE = r.get("Process")
    TIMESTAMPS = r.get("Timestamps")
    FILENAMES = r.get("FileNames")
    USERNAME = r.get("User")

    check = data_validation(r)

    pro = ImageProcessor()
    processing_times = []
    processed_images = []
    processed_height = []
    processed_width = []
    OG_height = []
    OG_width = []

    OG_histograms = []
    proc_histograms = []

    if check:
        for x in range(len(IMAGES)):

            byte_image = base64.b64decode(IMAGES[x])
            i = decodeImage(byte_image)

            OG_histograms.append(pro.histogram(i))

            start = time.time()
            processed_image = process(i, PROCESSING_TYPE, pro)
            enc_image = cv2.imencode('.jpg', processed_image)
            end = time.time()

            proc_histograms.append(pro.histogram(processed_image))

            proc_time = end-start
            proc_time = float("{0:.4f}".format(proc_time))

            processing_times.append(proc_time)

            OG_characteristics = getImageCharacteristics(i)
            OG_height, OG_width = addImageCharacteristics(
                OG_characteristics, "original", OG_height, OG_width)
            proc_characteristics = getImageCharacteristics(processed_image)
            processed_height, processed_width = addImageCharacteristics(
                proc_characteristics, "processed", processed_height,
                processed_width)

            encoded_proc_img = encodeImage(enc_image[1])
            processed_images.append(encoded_proc_img)

        addImagesToDatabase(IMAGES, FILENAMES, USERNAME, processing_times,
                            PROCESSING_TYPE, OG_height, OG_width,
                            processed_height, processed_width, TIMESTAMPS)
        r2 = server_gui(IMAGES, TIMESTAMPS, OG_height, OG_width,
                        processed_images, processing_times, processed_height,
                        processed_width, OG_histograms, proc_histograms)
        return r2
    return "Bad Data send new Image(s) or Modified Version of Image"


def data_validation(dict):
    """
        Checks that data received from the gui is not Null
    :param dict: dictonary of usable information about the image
    from the gui
    :return: boolean
    """
    s1 = dict.get("Images")
    s2 = dict.get("Process")
    s3 = dict.get("Timestamps")
    if s1 is not None and s2 is not None and s3 is not None:
        return True
    return False


def addImagesToDatabase(IMAGES, FILENAMES, USERNAME, processing_times,
                        PROCESSING_TYPE, OG_height, OG_width,
                        processed_height, processed_width, TIMESTAMPS):
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
    img_char = img.shape

    return img_char


def addImageCharacteristics(img_char, img_type, height, width):
    """Adds the image characteristics (made from getImageCharacteristics
    function) to the global image characteristic variables
    :param img_char:
    :param img_type:
    :return:
    """

    if img_type == "original":
        height.append(img_char[0])
        width.append(img_char[1])

    elif img_type == "processed":
        height.append(img_char[0])
        width.append(img_char[1])
    return height, width


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


def server_gui(Images, Timestamps, og_height, og_width,
               Pro_images, Pro_times, pro_height, pro_width,
               og_histo, pro_histo):
    """
        Packs the data for the processed image into a dict
        to be sent back to the gui

    :param Images: list of encoded og images
    :param Timestamps: list of datatime objects, when images
    were uploaded
    :param og_height: list that contains the orginal images
    heights
    :param og_width: list that contains the original image
    widths
    :param Pro_images: list of encoded processed images
    :param Pro_times: list of times that it took to process
    the image
    :param pro_height: list that contains the processed
    image's heights
    :param pro_width: list that contains the processed
    image's widths
    :param og_histo: list that contains the histograms
    for the original image channels
    :param pro_histo: list that contains the histograms
    for the processed image channels
    :return: dict that contains the all the information
    described above
    """
    return_data = {
        "OG Images": str(Images),
        "Timestamps": str(Timestamps),
        "OG Height": str(og_height),
        "OG Width": str(og_width),
        "Processed Images": str(Pro_images),
        "Time Spent": str(Pro_times),
        "Processed Height": str(pro_height),
        "Processed Width": str(pro_width),
        "OG Histograms": json.dumps(og_histo),
        "Processed Histograms": json.dumps(pro_histo)
    }
    r = json.dumps(return_data)

    return r


if __name__ == "__main__":
    app.run(host="0.0.0.0")
