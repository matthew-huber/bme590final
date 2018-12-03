from image_processor_server import *
import pytest
import numpy as np
import datetime as dt
import base64


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
    (b'010101010111', "MDEwMTAxMDEwMTEx"),
    (b'0101', "MDEwMQ=="),
    (b'0101110', "MDEwMTExMA==")
])
def test_encodeImage(img, base64_string):
    assert encodeImage(img) == base64_string
