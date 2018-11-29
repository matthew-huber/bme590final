import pytest
from ImageProcessor import ImageProcessor


@pytest.fixture
def IP():
    IP = ImageProcessor()
    return IP
