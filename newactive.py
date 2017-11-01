# noinspection PyCompatibility
import configparser
import datetime
import platform

from SMS_send import SMSSend
from SMSblessing_stone import stoneobject
from TimerTask import Task
from blessing_main import BlessingPlay
from email_send import EmailSend
from loading import Loading
from mylogger import Logger

if __name__ == '__main__':
    # 记录器 实例
    logname = "生日、司龄祝福短信日志"
    log = Logger(logname)
    logger = log.getlogger()
    # 解析器实例
    conf = configparser.ConfigParser()
    if platform.system() == 'Windows':
        conf.read("SMSblessing.conf", encoding="utf-8-sig")
    else:
        conf.read("SMSblessing.conf")
    # 数据库实例
    stone = stoneobject()
    # 初始化 定时器
    task = Task("08:00", logger)
    times = conf.get(section="time", option="now")
    if task.times != datetime.time(int(times.split(':')[0]), int(times.split(':')[1])):
        task.times = input("请输入开始时间，例如08:00")
    # task.times = "19:45"
    logger.debug("主程序开始运行")
    # 初始化 邮件发送、短信发送
    send_mail = EmailSend(smtp_server=conf.get(section='email', option='smtp_server'),
                          smtp_port=conf.get(section='email', option='smtp_port'),
                          from_addr=conf.get(section='email', option='from_addr'),
                          from_addr_str=conf.get(section='email', option='from_addr_str'),
                          password=conf.get(section='email', option='password'), logger=logger, stone=stone)
    send_sms = SMSSend(logger=logger, stone=stone, apikey=conf.get(section='SMSServer', option='apikey'))
    loading = Loading(stone=stone, logger=logger, path='祝福短信人员.xls')
    while True:
        # 到达预定时间后，执行 BlessingPlay.play
        task.run(BlessingPlay.play, to_address=conf.get(section='options', option='to_addr'), logger=logger,
                 send_mail=send_mail, send_sms=send_sms, loading=loading, )
        logger.debug("当次执行完毕")
