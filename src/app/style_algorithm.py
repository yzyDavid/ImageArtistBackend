import numpy as np

from .algorithm import Algorithm


# noinspection PyCompatibility
class StyleAlgorithm(Algorithm):
    """
    First dirty impl.
    invoke by shell, maybe having perf problems.
    """
    def __init__(self):
        super().__init__()
        self.model_pathname = ''

    def serve(self, item: dict):
        """

        :param item: { 'img': str, 'style': str }
        :return: file_path_name: str
        """
        template_cmdline = \
            r'python main.py eval --content-image {} --style-image {} --model {} --content-size 1024'
        if 'img' not in item or 'style' not in item:
            raise KeyError('Argument Error')

    def run(self, img: np.ndarray, style: np.ndarray) -> np.ndarray:
        raise NotImplementedError
