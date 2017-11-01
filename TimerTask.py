import datetime

import time

class Task(object):

    def __init__(self, times, logger):
        """
        定时器
        :param times: 预定日期
        :param logger:记录器 实例
        """
        # print(type(datetime.time(int(times.split(':')[0]), int(times.split(':')[1]))))
        # print(datetime.time(int(times.split(':')[0]), int(times.split(':')[1])))
        self.times = times
        self.logger = logger
        pass

    def wait(self):
        """
        休眠
        :return:
        """
        # self.logger.debug("开始休眠")
        time.sleep(self._timer())
        pass

    def run(self, function_name, **kwargs):
        """
        到了预定时间后，运行 function_name 函数
        :param function_name: 到预定时间，执行的函数
        :param kwargs: function_name 的参数
        :return:
        """
        # print(self._timer())
        if 60*1 >= self._timer():
            self.logger.debug("已到预定时间，开始执行任务")
            return function_name(**kwargs)
        else:
            self.logger.debug("未到达预定时间，开始休眠{num}s".format(num=self._timer()))
            self.wait()
            self.run(function_name, **kwargs)
        pass

    @property
    def times(self):
        """
        x.times 等于  x.gettimes()
        :return:
        """
        return self._times
        pass

    @times.setter
    def times(self, times):
        """
        x.times = "xxx"  等于 x.settimes("xxx")
        :param times:
        :return:
        """
        assert int(times.split(':')[0]) in range(23) and int(times.split(':')[1]) in range(60), "时间格式错误"
        print("赋值开始")
        self._times = datetime.time(int(times.split(':')[0]), int(times.split(':')[1]))
        pass

    '''
    返回现在时间和预定时间相差的秒数，参数使用datetime.time来构造
    如果今天超过预定时间，则返回距离明天预定时间相差的秒数
    例如：
    print(timer(datetime.time(8,00))) 误差应该是小于1s
    '''
    def _timer(self):
        """
        确定距离【预定时间】剩余多少秒，定时时间减少 10s 防止误差
        :return:
        """
        nowtime = datetime.datetime.now().time()
        if self.times > nowtime:
            return (self.times.hour - nowtime.hour) * 60 * 60 + (self.times.minute - nowtime.minute) * 60 + (
                self.times.second - nowtime.second) - 10
        else:
            return (self.times.hour - nowtime.hour) * 60 * 60 + (self.times.minute - nowtime.minute) * 60 + (
                self.times.second - nowtime.second) + 60 * 60 * 24 - 10

