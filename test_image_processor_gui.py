import numpy as np
import pytest
from image_processor_gui import *


@pytest.mark.parametrize("input_img, expected_img", [
    (np.array([np.array([np.array([1, 2, 3])])]),
     np.array([np.array([np.array([3, 2, 1])])])),

    (np.array([np.array([np.array([3, 2, 1])])]),
     np.array([np.array([np.array([1, 2, 3])])])),

    (np.array([np.array([np.array([10, 25, 3])])]),
     np.array([np.array([np.array([3, 25, 10])])])),
])
def test_compress_multidimm_image(input_img, expected_img):
    assert(np.array_equal(compress_multidimm_image(input_img),expected_img))


@pytest.mark.parametrize("filenames, username, expected", [
    (["file_name"], "katelyn", ["file_namekatelyn"]),
    (["random/file"], "katelyn", ["filekatelyn"]),
    (["long/path/test"], "katelyn", ["testkatelyn"])
])
def test_makeDatabaseFileNames(filenames, username, expected):
    assert makeDatabaseFileNames(filenames, username) == expected


@pytest.mark.parametrize("filenames, expected", [
    (["simple_path"], ["simple_path"]),
    (["/longer/path/with/stuff"], ["stuff"]),
    (["has/some//double//slashes///blah"], ["blah"])
])
def test_getfilenames_remove_full_path(filenames, expected):
    assert get_filenames_remove_full_path(filenames) == expected


@pytest.mark.parametrize("files, username, expected", [
    (["/file/with/slashes"], "katelyn", ["/file/with/slasheskatelyn"]),
    (["random_file"], "blah", ["random_fileblah"]),
    (["another_test"], "hi", ["another_testhi"])
])
def test_get_files_add_username(files, username, expected):
    assert get_filenames_add_username(files, username) == expected


@pytest.mark.parametrize("filepath, isValid", [
    ("TestImages/color_img.jpg", True),
    ("TestImages/GS_2D.png", True),
    ("TestImages/not_an_image.png", False)
])
def test_validateImageHeader(filepath, isValid):
    assert validateImageHeader(filepath) == isValid


@pytest.mark.parametrize("input_files, output_files", [
    (["TestImages/not_an_image.png"], []),
    (["TestImages/GS_2D.png", "TestImages/GS_2D.png"],
     ["TestImages/GS_2D.png", "TestImages/GS_2D.png"]),
    (["TestImages/GS_2D.png", "TestImages/not_an_image.png",
      "TestImages/color_img.jpg"],
     ["TestImages/GS_2D.png", "TestImages/color_img.jpg"])
    ])
def test_validateFiles(input_files, output_files):
    assert validateFiles(input_files) == output_files
