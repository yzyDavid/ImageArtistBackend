class Algorithm(object):
    """
    Abstract class for algorithms.
    """
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        if type(args[0]) == dict:
            return self.serve(args[0])
        else:
            return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        """
        run the algorithm, with prepared data.
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def serve(self, item: dict):
        """
        should be invoked from web, pre process data and invoke run to do the actual things.
        :param item:
        :return:
        """
        raise NotImplementedError
