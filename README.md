# 生日、司龄祝福自动发送项目

## 更新

2017-12-28 更新短信模板，以及更新人员信息

## 使用

项目运行 `Python newactive` 默认定时为8:00，使用`task.times = "19:45"`来修改定时时间

使用了 jinja2 、 sqlalchemy 、 [chinesecalendar](https://github.com/LKI/chinese-calendar) 模块 ，使用云片网发送短信。基于Python3.6

## 文件说明

【newactive.py】 实现资源申明、定时开始时间

【blessing_main】 实现业务逻辑（即需求），细节详见【loading.py】、【email_send.py】、【SMS_send.py】

【SMSblessing_stone.py】 申明了【员工信息表】、【司龄表】、【生日表】

【loading.py】 实现 excel 数据转到 sqlite 数据库【员工信息表】中 ，同时查询数据将符合日期的人员放到 【司龄表】或【生日表】中

【blessingsend.py】 申明了发送的3个函数 获取模板【_get_template()】、获取数据【_get_data()】、发送【send()】

【email_send.py】 继承了【blessingsend.py】，并实现了相关细节

【SMS_send.py】 继承了【blessingsend.py】，并实现了相关细节

【TimerTask.py】 实现定时功能

【mylogger.py】 实现了自己的日志记录

【templates/blessing.html】 邮件模板

【constants.py】 短信模板

【data_pull.py】 多个excel花名册 整合成一个 表格样式如下

| 工号        | 姓名           | 虚拟入职时间  | 出生年月 | 联系方式 |
|:----------:|:----:|:----------:|:----------:|:-----------:|
|12XXXXXXXX| XXX           | 2016-12-28  | 1994-12-28 | 132XXXXXXXX |

【SMSblessing.conf】 配置文件 格式如下

```
[options]
to_addr =
error_addr = 


[time]
now=08:00


[email]
smtp_server = 
smtp_port = 
# SSL 端口
from_addr = 
from_addr_str = 祝福管理站
password = 

[SMSServer]
apikey = 
#云片网 apikey
```

## 需求：

1. 每日早上8:00定时发送【短信】、【邮件】（非工作日不要发送邮件；最后一个工作日要将至下个工作日之间的生日、司龄人员进行发送

2. 花名册中非【离职】、【司龄补回】sheet所有名单

3. 邮件中必须要有【工号】、【姓名】、【发送日期】、【司龄】、【电话号码】

4. 短信分为【司龄】、【生日】模板


## 实现思路：


1. 从花名册获取人员数据存储至 excle 中 。主要获取的信息为【工号】、【姓名】、【虚拟入职日期】、
【出生年月】、【联系方式】


2. 将数据读取到数据库中，根据需求进行发送【短信】、【邮件】


