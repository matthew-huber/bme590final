import pytest
from ImageProcessor import ImageProcessor
from image_processor_gui import App


@pytest.fixture
def IP():
    IP = ImageProcessor()
    return IP


@pytest.fixture
def GUI():
    GUI = App()
    return GUI
