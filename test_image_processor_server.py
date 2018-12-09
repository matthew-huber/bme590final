from image_processor_server import *
import pytest
import numpy as np
import datetime as dt
import base64
import matplotlib.image as mpimg
import json
from datetime import datetime
from ImageProcessor import *
import skimage as ski


@pytest.mark.parametrize("dict, is_valid", [
    ({}, False),
    ({"Images": np.array(3), "Process": "Histogram Equalization",
      "Timestamps": dt.datetime.now()}, True),
    ({"Images": np.array(3), "Process": None,
      "Timestamps": dt.datetime.now()}, False),
    ({"Process": "Histogram Equalization"}, False),
    ({"Images": np.array(3), "Process": "Histogram Equalization"}, False),
    ({"Process": "Histogram Equalization"}, False)
])
def test_data_validation(dict, is_valid):
    assert data_validation(dict) == is_valid


@pytest.mark.parametrize("img, height, width", [
    (np.zeros(shape=(5, 2)), 5, 2),
    (np.zeros(shape=(5, 2, 10)), 5, 2),
    (np.zeros(shape=(10, 12, 3)), 10, 12)
])
def test_getImageCharacteristics(img, height, width):
    img_char = getImageCharacteristics(img)
    assert img_char[0] == height
    assert img_char[1] == width


@pytest.mark.parametrize("img", [
    (np.array([1, 2, 3])),
    (np.array([1, 2, 2, 5, 6])),
    (np.array([np.array([1, 2, 2, 5, 6, 8, 10])]))
])
def test_encodeImage(img):
    bytes_img = img.tobytes()
    processed_img_base64 = base64.b64encode(bytes_img)
    base64_string = processed_img_base64.decode('ascii')
    assert encodeImage(img) == base64_string


# with open("TestImages/grayscale.jpeg", "rb") as image_file:
    # image_bytes = image_file.read()
# with open("TestImages/GS_3D.jpg", "rb") as image_file1:
    # image_bytes1 = image_file1.read()
# with open("TestImages/color_img.jpg", "rb") as image_file2:
    # image_bytes2 = image_file2.read()


# @pytest.mark.parametrize("img, base64_string", [
    # (image_bytes, mpimg.imread("TestImages/grayscale.jpeg", format='JPG')),
    # (image_bytes1, mpimg.imread("TestImages/GS_3D.jpg", format='JPG')),
    # (image_bytes2, mpimg.imread("TestImages/color_img.jpg", format='JPG')),
# ])
# def test_decodeImage(img, base64_string):
    # a = decodeImage(img) == base64_string
    # assert a.all()


@pytest.mark.parametrize("img, type1, height, width, list1, list2", [
    ([10, 5], "original", [], [], [10], [5]),
    ([11, 0], "processed", [], [], [11], [0]),
    ([17, 3], "original", [], [], [17], [3]),
])
def test_addimagechars(img, type1, height, width, list1, list2):
    val1, val2 = addImageCharacteristics(img, type1, height, width)
    boo1 = (val1 == list1)
    boo2 = (val2 == list2)
    boof = (boo1 and boo2)
    assert boof


@pytest.mark.parametrize("img, timestamps, og_height, og_width, pro_images,"
                         " pro_times, pro_height, pro_width,"
                         " og_histo, pro_histo, boo",
                         [
                            ([10, 5], [10], [10], [200], [200, 50], [10], [10],
                                [200], [10, 300], [30, 400], True),

                            ([10, 5], [20], [], [200], [200, 50], [10], [],
                             [200],
                                [10, 300], [30, 400], True),

                            ([], [20], [10], [200], [], [10], [10], [200],
                                [10, 300], [30, 400], True),
                         ])
def test_server_gui(img, timestamps, og_height, og_width, pro_images,
                    pro_times, pro_height, pro_width, og_histo,
                    pro_histo, boo):
    try:
        j = server_gui(img, timestamps, og_height, og_width,
                       pro_images, pro_times, pro_height,
                       pro_width, og_histo, pro_histo)
        json.loads(j)
    except ValueError:
        boof = False
    boof = True
    assert boof == boo


@pytest.mark.parametrize("images, filenames, username, pro_times, pro_type,"
                         " OG_height, OG_width, pro_height,"
                         " pro_width, timestamps, image_list1",
                         [
                            ([1], ["Test1"], "Mike", [.10], ["Histo_equal"],
                             [10], [10],
                                [200], [10], [str(datetime.now())],
                             ["Test1", "Test2", "Test3"]),

                            ([1], ["Test2"], "Mike", [.10], ["Histo_equal"],
                             [10], [10],
                                [200], [10], [str(datetime.now())],
                             ["Test1", "Test2", "Test3"]),

                            ([1], ["Test3"], "Mike", [.10], ["Histo_equal"],
                             [10], [10],
                                [200], [10], [str(datetime.now())],
                             ["Test1", "Test2", "Test3"]),
                         ])
def test_addimagestodatabase(images, filenames, username, pro_times, pro_type,
                             OG_height, OG_width, pro_height, pro_width,
                             timestamps, image_list1):
    addImagesToDatabase(images, filenames, username, pro_times, pro_type,
                        OG_height, OG_width, pro_height, pro_width, timestamps)
    image_list = []
    for image in DB_Image_Meta.objects.raw({"user": "Mike"}):
        image_list.append(image.img_file_path)
    assert image_list == image_list1


@pytest.mark.parametrize("img, proc_type, output", [
    (np.array([1, 2, 3]), "Histogram Equalization",
     np.array([0, 127, 255])),

    (np.array([1, 2, 2, 5, 6]), "Contrast Stretching",
     ski.exposure.rescale_intensity(np.array([1, 2, 2, 5, 6]))),

    (np.array([np.array([1, 2, 2, 5, 6, 8]), np.array([1, 2, 2, 5, 6, 8])]),
     "Log Compression",
     np.array([np.array([1, 2, 2, 7, 8, 11]),
               np.array([1, 2, 2, 7, 8, 11])])),
    (np.array([1, 2, 3]), "Reverse Video", np.array([-2, -3, -4])),
])
def test_process(img, proc_type, output, IP):
    assert np.array_equal(process(img, proc_type, IP), output)
