from sklearn.cluster import KMeans
import numpy as np
import cv2
import os

from .algorithm import Algorithm


# noinspection PyCompatibility
class ThemeAlgorithm(Algorithm):
    def __init__(self, num_colors=None):
        super().__init__()
        self.n_colors = num_colors if num_colors else 5

    def run(self, img: np.ndarray, num_colors: int = None) -> np.ndarray:
        n_colors = num_colors if num_colors else self.n_colors

        k_means = KMeans(n_clusters=n_colors)
        im = img.reshape(-1, 3)
        labels = k_means.fit_predict(im)

        themes = np.zeros((n_colors, 3), dtype=np.uint64)
        counter = np.zeros((n_colors,), dtype=np.uint)
        for px, l in zip(im, labels):
            themes[l] += px
            counter[l] += 1
        for i in range(n_colors):
            themes[i] //= counter[i]

        color = np.zeros_like(im)
        for i in range(color.shape[0]):
            color[i] = themes[labels[i]]
        color = color.reshape(img.shape)

        return color

    def serve(self, item: dict) -> str:
        """

        :param item: { 'file': file_path_name, 'count': int [optional] }
        :return: processed file_path_name
        """
        f = item['file']
        im = cv2.imread(f, cv2.IMREAD_COLOR)

        if 'count' not in item:
            result = self.run(im)
        else:
            result = self.run(im, num_colors=item['count'])

        fn = f + '_PROCESSED.jpg'
        cv2.imwrite(fn, result)

        return fn
