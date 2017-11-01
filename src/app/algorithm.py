class Algorithm(object):
    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        """
        run the algorithm, with prepared data.
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def serve(self, item: dict) -> None:
        """
        should be invoked from web, pre process data and invoke run to do the actual things.
        :param item:
        :return:
        """
        raise NotImplementedError
