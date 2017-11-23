import datetime
from pprint import pprint

from sqlalchemy import and_

from SMSblessing_stone import Birthlist, Divisionlist
from blessingsend import Send
# noinspection PyCompatibility
from urllib.parse import quote
from yunpian_python_sdk.model import constant as yc
from yunpian_python_sdk.ypclient import YunpianClient


# noinspection PyCompatibility
class SMSSend(Send):
    # noinspection PyCompatibility
    def __init__(self, logger, stone, apikey, *args, **kwargs):
        """
        初始化【参数】，并获取模板
        :param logger: 记录器实例
        :param stone:数据库连接实例
        :param apikey:云片apikey
        """
        # noinspection PyCompatibility
        super().__init__(logger, stone, *args, **kwargs)
        self.logger = logger
        self.stone = stone
        self.siling_templates = None
        self.brith_templates = None
        self.brith_result = None
        self.siling_result = None
        self._get_template()
        self.clnt = YunpianClient(apikey)

    def send(self, today):
        """
        根据发送日期，获取数据后填充至模板，并对发送的模板进行编码。
        :param today: 发送日期
        :return:
        """
        self.logger.debug("开始发送短信")
        self._get_data(today=today, days=1)
        tel = []
        data_str = []
        sms_result_dict = {'siling': self.siling_result, 'brith': self.brith_result}
        sms_templates_dict = {'siling': self.siling_templates, 'brith': self.brith_templates}
        for key, value in sms_result_dict.items():
            if len(value):
                for one in value:
                    tel.append(one.Tel)
                    data_str.append(sms_templates_dict[key][one.flagnum].format(Name=one.name, Day=today))
        # pprint(data_str)
        if len(tel) and len(data_str):
            param = {yc.MOBILE: ','.join(tel), yc.TEXT: (','.join(self._sms_send(data_str)))}
            # r = self.clnt.sms().multi_send(param)
            self.clnt.sms().multi_send(param)
        self.logger.debug("短信发送完成")
        pass

    def _get_template(self):
        """
        获取模板,因list第一个是从0开始，所有空置第一个元素
        所有的模板均是文本格式，参数有2个 Name 、 Day
        :return:
        """
        self.logger.debug("短信模板获取开始")
        siling = ["", ]
        brith = ["", ]
        file = open('司龄祝福', 'rb')
        for f in file.readlines():
            siling.append(f.decode('utf-8').replace('\r\n', '', -1))
        file = open('生日祝福', 'rb')
        for f in file.readlines():
            brith.append(f.decode('utf-8').replace('\r\n', '', -1))
        # return siling, brith
        self.siling_templates = siling
        self.brith_templates = brith
        self.logger.debug("短信模板获取完成")
        pass

    def _get_data(self, today, days):
        # 相对于【邮件发送】，【短信发送】只需要考虑当天发送，具体实现方式在 【send】 中体现
        self.logger.debug("开始获取短信数据")
        table_dict = {'brith_result': Birthlist, 'siling_result': Divisionlist}
        # 使用list 相加的功能，形成不嵌套的list
        brith_result = []
        siling_result = []
        result_dict = {'brith_result': brith_result, 'siling_result': siling_result}
        for key, value in table_dict.items():
            for i in range(days):
                result = self.stone.query(value).filter(
                    and_(value.date == today + datetime.timedelta(days=i), value.status == True)).all()
                if len(result):
                    result_dict[key] += result
        self.brith_result = brith_result
        self.siling_result = siling_result
        self.logger.debug("短信数据获取完成")
        pass

    @staticmethod
    def _sms_send(array):
        data_str = []
        for one in array:
            data_str.append(quote(one))
        return data_str
        pass

    pass
