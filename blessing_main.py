import datetime
import time

from chinese_calendar import is_workday, is_holiday


class BlessingPlay(object):
    def __init__(self):
        pass

    @classmethod
    def _workexec(cls, today):
        """
        类方法，不需要实例化
        功能 ： 判断今天是不是工作日
        :param today:开始日期
        :return:
        """
        # march_first = datetime.date.today()
        # i=0
        days = 0
        march_first = today
        while True:
            print(is_workday(march_first))  # False
            print(is_holiday(march_first))  # True
            days = days + 1
            march_first = today + datetime.timedelta(days=days)
            if is_workday(march_first):
                break
        return days

    @classmethod
    def play(cls, to_address, logger, send_mail, send_sms, loading, ):
        """
        类方法，不需要实例化
        功能：
        1、判断今天是不是工作日
        2、判断今天之后 days 天为工作日
        3、实例化 class Loading 对象loading ，并进行数据处理 run
        4、今天是工作日则发送 1 + days 天的邮件，否则跳过
        5、发送当天的短信
        6、休眠23H
        :param to_address:收件地址
        :param logger:记录器实例
        :param send_mail:邮件发送实例
        :param send_sms:短信发送实例
        :param loading:数据处理实例
        :return:
        """
        #  需要执行的动作
        # 工作日判断
        today = datetime.date.today()
        days = cls._workexec(today)
        logger.debug("查询日期天数:{day}".format(day=days))
        # 数据读取以及处理
        logger.debug("开始数据读取和处理")
        loading.run(days=days, today=today)
        logger.debug("数据读取和处理已结束")
        # logger.debug("执行邮件和短信发送")
        if is_workday(datetime.date.today()):
            send_mail.send(header='祝福短信{day}'.format(day=datetime.date.today()),
                           to_address=to_address, today=today, days=days, )
        send_sms.send(today=today, )
        logger.debug("执行完毕开始休眠23H")
        time.sleep(60 * 60 * 23)

