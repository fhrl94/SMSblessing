import datetime

import xlrd
from sqlalchemy import text

from SMSblessing_stone import EmployeeInfo, Birthlist, Divisionlist


class Loading(object):

    def __init__(self, stone, logger, path, ):
        """
        初始化 数据库连接，并将上次运行的遗留数据进行删除
        :param stone:数据库连接
        :param logger:记录器实例
        :param path:excel文件路径
        """
        self.stone = stone
        self.logger = logger
        self.path = path
        self.stone.query(EmployeeInfo).delete()
        self.stone.commit()
        self._create_data()
        self.logger.debug("数据库 EmployeeInfo 初始化完成")

    def run(self, days, today):
        """

        :param days:距起始日期的天数
        :param today:起始日期
        :return:
        """
        self._data_delete()
        self.stone.commit()
        self.logger.debug("已删除上次 Birthlist 、Divisionlist 数据")
        for i in range(days):
            self._transform(i=i, today=today)
        self.logger.debug("已更新本次 Birthlist 、Divisionlist 数据")
        pass

    def _create_data(self):
        """
        将 excel 中原始数据读取到数据库
        list 对象 cols 中存储的是列信息，要与 excel 表列保持一致
        :return:
        """
        def _one_or_none(obj):
            if obj == '':
                return None
            else:
                return obj

        workbook = xlrd.open_workbook(self.path)
        cols = ['code', 'name', 'enterdate', 'birthDate', 'Tel', ]
        for count, one in enumerate(workbook.sheet_names()):
            for i in range(1, workbook.sheet_by_name(one).nrows):
                if workbook.sheet_by_name(one).ncols > 7:
                    print('错误')
                    break
                empinfo = EmployeeInfo()
                setattr(empinfo, 'id', i)
                setattr(empinfo, 'Cover', None)
                print(i)
                for j, col in enumerate(cols):
                    print(j)
                    if col == 'enterdate' or col == 'birthDate':
                        if _one_or_none(workbook.sheet_by_name(one).cell_value(i, j)):
                            setattr(empinfo, col,
                                    datetime.datetime.strptime(
                                        workbook.sheet_by_name(one).cell_value(i, j), '%Y-%m-%d'))
                        else:
                            setattr(empinfo, col, None)
                    elif col == 'code' or col == 'Tel':
                        # 0开始的工号处理
                        if len(str(int(_one_or_none(workbook.sheet_by_name(one).cell_value(i, j))))) < 10 \
                                and col == 'code':
                            setattr(empinfo, col,
                                    '0' + str(int(_one_or_none(workbook.sheet_by_name(one).cell_value(i, j)))))
                        else:
                            setattr(empinfo, col, int(_one_or_none(workbook.sheet_by_name(one).cell_value(i, j))))
                    elif col == 'name':
                        setattr(empinfo, col, _one_or_none(workbook.sheet_by_name(one).cell_value(i, j)))
                # print(empinfo.__dict__)
                # print(type(empinfo))
                self.stone.add(empinfo)
            self.stone.commit()

        pass

    def _transform(self, i, today,):
        """
        在 EmployeeInfo 根据起始日期、距起始日期天数，获取起始日期之后 i 天的人员名单(生日、司龄)
        可以对这个过程抽象，但是意义不大
        :param i:距起始日期天数
        :param today:起始日期
        :return:
        """
        result = self.stone.query(EmployeeInfo).filter(
            text("strftime('%m%d',DATE (birthDate,'1 day'))=strftime('%m%d',date(:date,:value)) ")).params(
            value='{0} day'.format(i + 1), date=today).all()
        # result=stone.query(EmployeeInfo).filter(text("id=(':value')")).params(value=224)
        # print(result.one())
        for one in result:
            # print(one)
            birth = Birthlist()
            # 处理后缀数值
            try:
                int(one.name[len(one.name) - 1])
                birth.name = one.name[:len(one.name) - 1]
            except ValueError:
                birth.name = one.name
            birth.code = one.code
            birth.birthDate = one.birthDate
            birth.Tel = one.Tel
            birth.flagnum = today.month
            birth.date = today + datetime.timedelta(days=i)
            birth.status = True
            # 可能会出现重复值
            self.stone.add(birth)
        self.stone.commit()
        # print('_________')
        result = self.stone.query(EmployeeInfo).filter(
            text("strftime('%m%d',DATE (enterdate,'1 day'))=strftime('%m%d',date(:date,:value)) ")).params(
            value='{0} day'.format(i + 1), date=today).all()
        for one in result:
            # print(one)
            division = Divisionlist()
            # 处理后缀数值
            try:
                int(one.name[len(one.name) - 1])
                division.name = one.name[:len(one.name) - 1]
            except ValueError:
                division.name = one.name
            division.code = one.code
            division.realityenterdate = one.enterdate
            division.Tel = one.Tel
            division.flagnum = today.year - one.enterdate.year
            division.date = today + datetime.timedelta(days=i)
            division.status = True
            self.stone.add(division)
        self.stone.commit()
        pass

    def _data_delete(self):
        """
        删除 Birthlist 、Divisionlist （生日、司龄名单）
        :return:
        """
        self.stone.query(Birthlist).delete()
        self.stone.query(Divisionlist).delete()
        self.stone.commit()
        pass

    pass

