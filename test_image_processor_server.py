from image_processor_server import *
import pytest
import numpy as np
import datetime as dt
import base64
import matplotlib.image as mpimg


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
    assert img_char["height"] == height
    assert img_char["width"] == width


@pytest.mark.parametrize("img, base64_string", [
    (np.array([1, 2, 3]), 'AQAAAAAAAAACAAAAAAAAAAMAAAAAAAAA'),
    (np.array([1, 2, 2, 5, 6]), "AQAAAAAAAAACAAAAAAAAAAIAAAAA"
                                "AAAABQAAAAAAAAAGAAAAAAAAAA=="),
    (np.array([np.array([1, 2, 2, 5, 6, 8, 10]), np.array([1, 2,
                                                           2, 5, 6,
                                                           8, 10])]), "AQAAA"
                                                                      "AAAAA"
                                                                      "ACAAA"
                                                                      "AAAA"
                                                                      "AAAIA"
                                                                      "AAAA"
                                                                      "AAA"
                                                                      "ABQAAA"
                                                                      "AAAA"
                                                                      "AAGA"
                                                                      "AAAAAA"
                                                                      "AAAgAAA"
                                                                      "AAAA"
                                                                      "AACgAA"
                                                                      "AAAAAAA"
                                                                      "BAAAAA"
                                                                      "AAAA"
                                                                      "AIAAA"
                                                                      "AAAA"
                                                                      "AAAgA"
                                                                      "AA"
                                                                      "AAAAA"
                                                                      "AFAA"
                                                                      "AAAA"
                                                                      "AAAAY"
                                                                      "AAAAA"
                                                                      "AAAACA"
                                                                      "AAAAA"
                                                                      "AAAAK"
                                                                      "AAAAA"
                                                                      "AAA"
                                                                      "AA==")
])
def test_encodeImage(img, base64_string):
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


@pytest.mark.parametrize("img, type1, base64_string", [
    ([10, 5], "original", True),
    ([11, 0], "processed", True),
    ([11, 0], " ", False),
])
def test_addimagechars(img, type1, base64_string):
    val = addImageCharacteristics(img, type1)
    assert val == base64_string
