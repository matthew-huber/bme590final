import pytest
from ImageProcessor import ImageProcessor
from image_processor_gui import App
import numpy as np


@pytest.fixture
def IP():
    IP = ImageProcessor()
    return IP


@pytest.fixture
def GUI():
    GUI = App()
    return GUI
