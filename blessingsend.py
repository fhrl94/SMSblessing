class Send(object):
    def __init__(self, logger, stone, *args, **kwargs):
        """
        初始化，最少要初始化 【记录器】、【数据库连接】，同时获取模板,并初始化
        :param logger: 记录器实例
        :param stone:数据库连接实例
        :param args:
        :param kwargs:
        """
        self.logger = logger
        self.stone = stone
        self._get_template()

    def send(self, *args, **kwargs):
        """
        祝福发送的主要方法，子类根据各自需求，调用 _get_template() 、 _get_data() ，实现模板获取和数据获取，将数据填充
        至模板中，并发送
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplemented
        pass

    def _get_template(self, *args, **kwargs):
        """
        实现模板获取
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplemented
        pass

    def _get_data(self, *args, **kwargs):
        """
        实现数据获取
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplemented
        pass

        # def get_arguments(self):
        #     raise NotImplemented
        #     pass
