# 导入:
import sqlite3

import sys
from sqlalchemy import Column, create_engine, Date, BOOLEAN, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

cx = sqlite3.connect(sys.path[0]+"/emp.sqlite3")
engine = create_engine("sqlite:///"+sys.path[0]+"/emp.sqlite3", echo=True)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 创建对象的基类:
Base = declarative_base()
# 连接数据库
session = DBSession()

# 定义User对象:
class EmployeeInfo(Base):
    # 表的名字:
    __tablename__ = 'EmployeeInfo'

    # 表的结构:
    id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    code = Column(String(10))
    enterdate = Column(Date())
    # Divisiondates = Column(Date())
    birthDate = Column(Date())
    Tel = Column(String(11))
    # leaveDate = Column(Date())
    # Cover = Column(Integer())

    def __str__(self):
        return self.name

class Birthlist(Base):
    # 表的名字:
    __tablename__ = 'Birthlist'

    # 表的结构:
    id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    code = Column(String(10))
    birthDate = Column(Date())
    Tel = Column(String(11))
    flagnum = Column(Integer())
    date = Column(Date())
    status = Column(BOOLEAN())

    def __str__(self):
        return self.name


class Divisionlist(Base):
    # 表的名字:
    __tablename__ = 'Divisionlist'

    # 表的结构:
    id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    code = Column(String(10))
    realityenterdate = Column(Date())
    Tel = Column(String(11))
    flagnum = Column(Integer())
    date = Column(Date())
    status = Column(BOOLEAN())

# class Divisionlist(Base):
#     # 表的名字:
#     __tablename__ = 'Divisionlist'
#
#     # 表的结构:
#     id = Column(Integer(), primary_key=True)
#     name = Column(String(20))
#     code = Column(String(10))
#     realityenterdate = Column(Date())
#     Tel = Column(String(11))


# 如果没有创建表，则创建
Base.metadata.create_all(engine)


def stoneobject():
    return session
