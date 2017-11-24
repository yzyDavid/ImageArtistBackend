import numpy as np
import os

from .algorithm import Algorithm
from styl.experiments.main import entry, get_context


# noinspection PyCompatibility
class StyleAlgorithm(Algorithm):
    """
    First dirty impl.
    invoke by shell, maybe having perf problems.
    """

    def __init__(self):
        super().__init__()
        self.model_pathname = 'styl/experiments/models/21styles.model'
        self.output_pathname = 'output.jpg'
        self.main_python = 'styl/experiments/main.py'

        self.context = get_context()

    @DeprecationWarning
    def _serve(self, item: dict):
        """
        receive two file path name and return a file path name.
        :param item: { 'img': str, 'style': str }
        :return: file_path_name: str
        """
        template_cmdline = \
            r'python %s eval --content-image %s --style-image %s --model %s --content-size 1024'
        if 'img' not in item or 'style' not in item:
            raise KeyError('Argument Error')

        cmdline = template_cmdline % (self.main_python, item['img'], item['style'], self.model_pathname)
        os.system(cmdline)
        return self.output_pathname

    def serve(self, item: dict):
        """
        receive two file path name and return a file path name.
        :param item: { 'img': str, 'style': str }
        :return: file_path_name: str
        """
        if 'img' not in item or 'style' not in item:
            raise KeyError('Argument Error')

        entry(item['img'], item['style'], *self.context)
        return self.output_pathname

    def run(self, img: np.ndarray, style: np.ndarray) -> np.ndarray:
        raise NotImplementedError
