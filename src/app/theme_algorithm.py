from sklearn.cluster import KMeans
import numpy as np
import cv2

from .algorithm import Algorithm


# noinspection PyCompatibility
class ThemeAlgorithm(Algorithm):
    def __init__(self, num_colors=None):
        super().__init__()
        self.n_colors = num_colors if num_colors else 5

    def run(self, img: np.ndarray, num_colors: int) -> np.ndarray:
        n_colors = num_colors if num_colors else self.n_colors
        return img  # TODO

    def serve(self, item: dict):
        """

        :param item: { 'file': file_path_name }
        :return: processed file_path_name
        """
        f = item['file']
        im = cv2.imread(f, cv2.IMREAD_COLOR)
