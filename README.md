# webserver
分析新闻和微博数据

需要在项目目录中添加配置文件 config.py 格式如下


import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = 'hard'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SUBJECT_PREFIX = 'Center'
    MAIL_SENDER = 'YOUR EMAIL'
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'YOUR EMAIL'
    MAIL_PASSWORD = 'PASSWORD'
    MAIL_USE_SSL = True

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @staticmethod
    def init_app(app):
        pass



在app目录下新建static目录存放js css bootstrap echarts jquery等
