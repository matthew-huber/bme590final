import skimage as ski
import numpy as np


class ImageProcessor:
    """ImageProcessor is a class that implements the image processing
    functions from scikit-image. It has no input parameters for the
    construction and does not have any attributes.
    """

    def __init__(self):
        pass

    def histogramEqualization(self, img):
        """Applies histogram equalization to input image

        :param img: Image be processed
        :return: hist_eql_img: img after histogram equalization
        """
        hist_eql_img = ski.exposure.equalize_hist(img)
        return hist_eql_img

    def contrastStretch(self, img):
        """Applies contrast stretching to input image

        :param img: Image to be processed
        :return: cont_stretch_img: img after contrast stretching
        """
        cont_stretch_img = ski.exposure.rescale_intensity(img)
        return cont_stretch_img

    def logCompression(self, img):
        """Applies logarithmic compression to input image

        :param img: Image to be processed
        :return: log_comp_img: img after logarithmic compression
        """
        log_comp_img = ski.exposure.adjust_log(img)
        return log_comp_img

    def reverseVideo(self, img):
        is_gs = self.isGrayscale(img)
        if not is_gs:
            raise ValueError

        gs_inverted = np.invert(img)
        return gs_inverted

    def isGrayscale(self, img):
        """Checks to see if an image is grayscale

        isGrayscale determines if an images is grayscale by assuming a
        grayscale image will have one of the following properties
        1. Only have two dimensions
        2. If it has 3D (indicating RGB pixel color values), R=B=G for all
        pixels.

        :param img: Input image
        :return: is_grayscale: Indicates whether the input image is grayscale
        """

        if img.ndim == 2:
            is_grayscale = True
            return is_grayscale
        img_dimm = img.shape

        for x in range(0, img_dimm[0]):
            for y in range(0, img_dimm[1]):
                if img[x, y, 0] == img[x, y, 1] == img[x, y, 2]:
                    continue
                else:
                    is_grayscale = False
                    return is_grayscale

        # It makes it through the loop without finding a place where pixels
        # are not equal (causing it to return False), then assume that it is
        #  a grayscale image.
        is_grayscale = True
        return is_grayscale

    def histogram(self, img):
        """Generates a list of histograms with intensity values for each
        channel in the image.

        Each item in the list consists of a 2D numpy array, in which the
        first dimension is the histogram itself, and the second dimension
        is the bin values. A histogram item from this list could be plotted
        as plt.plot(histogram_item[1], histogram_item[0])

        :param img: input image
        :return: hist (list): List of histograms for each color channel
        """
        hist = []
        if self.isGrayscale(img):

            hist.append(ski.exposure.histogram(img))
            return hist
        else:
            dimm = img.shape
            hist = []
            for d in range(0, dimm[2]):
                h = ski.exposure.histogram(img[:, :, d])
                hist.append(h)
            return hist
