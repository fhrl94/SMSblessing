import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import os

import jinja2
from sqlalchemy import and_

from SMSblessing_stone import Birthlist, Divisionlist
from blessingsend import Send


class EmailSend(Send):
    def __init__(self, smtp_server, smtp_port, from_addr, from_addr_str, password, logger, stone, *args, **kwargs):
        """
        初始化 【参数】，并获取模板
        :param smtp_server: SMTP地址
        :param smtp_port: SMTP端口
        :param from_addr: 发件人邮箱
        :param from_addr_str: 发件人友好名称
        :param password: 发件人邮件密码
        :param logger: 记录器实例
        :param stone: 数据库实例
        """
        # noinspection PyCompatibility
        super().__init__(logger, stone, *args, **kwargs)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.from_addr = from_addr
        self.from_addr_str = from_addr_str
        self.password = password
        self.logger = logger
        self.stone = stone
        self.brith_result = None
        self.siling_result = None
        self.templates = None
        self._get_template()

    #  实现邮件发送
    def send(self, to_address, header, today, days):
        """
        先调用 _get_data() 获取数据，在调用 _get_template() 获取模板，并将数据进行填充。再调用 _email_send() 发送邮件
        顺序不能调整
        :param to_address: 收件人地址
        :param header:邮件主题【标题】
        :param today:开始日期
        :param days:至今天之后的天数，获取节假日【生日】、【司龄】人员
        :return:
        """
        self.logger.debug("开始发送邮件")
        self._get_data(today, days)
        # print(self._get_template())
        body = self.templates.render(brith_list=self.brith_result, siling_list=self.siling_result)
        self._email_send(to_address=to_address, header=header, body=body)
        self.logger.debug("邮件发送完成")

        pass

    #  实现数据获取
    def _get_data(self, today, days):
        """
        通过使用 【数据表】、【结果表】 2个字典，实现获取不同类型的数据，并进行存储
        :param today: 数据的起始日期
        :param days: 距离起始日期的天数
        :return:
        """
        # 生日名单 brith_result  司龄名单 siling_result
        self.logger.debug("开始获取邮件数据")
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
        self.logger.debug("邮件数据获取完成")
        # print(len(siling_result))
        pass

    #  实现模板获取
    def _get_template(self):
        # 使用 jinja2 生成邮件模板，并根据【数据获取】的结果进行填充
        # jinja2 需要定位到当前目录
        self.logger.debug("邮件模板获取开始")
        template_loader = jinja2.FileSystemLoader(searchpath=os.path.abspath(".") + os.sep + 'templates' + os.sep)
        template_env = jinja2.Environment(loader=template_loader)
        templates = template_env.get_or_select_template('blessing.html')
        # return templates
        self.templates = templates
        self.logger.debug("邮件模板获取完成")

    def _email_send(self, to_address, header, body, ):
        """
        邮件投递
        :param to_address: 收件人地址，格式为字符串，以逗号隔开
        :param header: 主题内容
        :param body: 正文内容
        :return: 无返回值
        """

        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        # 正文
        msg = MIMEText(body, 'html', 'utf-8')
        # 主题，
        msg['Subject'] = Header(header, 'utf-8').encode()
        # 发件人别名
        msg['From'] = _format_addr('{name}<{addr}>'.format(name=self.from_addr_str, addr=self.from_addr))
        # 收件人别名
        msg['To'] = to_address
        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, to_address.split(','), msg.as_string())
        server.quit()
        # print('邮件投递成功')
        # self.logger.info("邮件投递成功")

    pass
