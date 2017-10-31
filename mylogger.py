import logging
import os
from logging.handlers import TimedRotatingFileHandler


class Logger:

    def __init__(self, logname):
        self.filename = 'log' + os.sep + logname
        if not os.path.exists('log'):
            os.makedirs('log')
        # filename = 'log' + os.sep + "{day}.log".format(day=datetime.date.today())
        # 创建一个记录器【warning】
        self.logger = logging.getLogger("receive")
        # 设置日志等级【大于debug等级】
        self.logger.setLevel(logging.DEBUG)
        # 设置 日志处理器 Handler ；分3中【固定文件】、【按照文件大小切割】、【按时间切割】
        # fh = logging.FileHandler(filename=filename, encoding="utf-8")
        # fh = RotatingFileHandler(filename=filename, maxBytes=5*1024*1024, backupCount=5)
        self.fh = TimedRotatingFileHandler(filename=self.filename, when="D", encoding="utf-8")
        # 设置日志格式 【记录器名称 - 日期 - 等级 - 函数 - 消息】
        self.formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
        self.fh.setFormatter(self.formatter)
        # 设置过滤器【用"."分层】
        self.lfilter = logging.Filter(name="receive")
        self.logger.addHandler(self.fh)  # 为Logger实例增加一个处理器 handler
        self.logger.addFilter(self.lfilter)  # 为Logger实例增加一个过滤器 filter
        # logger.removeHandler(handler_name) # 为Logger实例删除一个处理器
        # 禁止输出日志
        # logger.disabled()

    def getlogger(self):
        return self.logger

    pass


