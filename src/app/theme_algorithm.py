from sklearn.cluster import KMeans
import numpy as np

from .algorithm import Algorithm


# noinspection PyCompatibility
class ThemeAlgorithm(Algorithm):
    def __init__(self):
        super().__init__()
        n_colors = 5

    def run(self, img: np.ndarray, num_colors: int) -> np.ndarray:
        pass
