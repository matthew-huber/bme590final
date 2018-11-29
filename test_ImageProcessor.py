from ImageProcessor import ImageProcessor
import pytest
from skimage import io


@pytest.mark.parametrize("file, is_gs_expected", [
    ("TestImages/GS_2D.png", True),
    ("TestImages/GS_3D.jpg", True),
    ("TestImages/color_img.jpg", False)
])
def test_isGrayscale(file, is_gs_expected, IP):
    img = io.imread(file)
    is_gs = IP.isGrayscale(img)

    assert is_gs_expected == is_gs
