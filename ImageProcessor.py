import skimage as ski


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