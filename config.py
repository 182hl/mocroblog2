import os


basedir = os.path.abspath(os.path.dirname(__file__))  #获取当前.py文件的绝对路径

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'microblog.env'))



# 使用类存储配置变量
class Config:
    # SECRET_KEY 这个配置变量，会被FLASK及其扩展使用其值作为加密密钥，用于生产签名或令牌，Flask-wtf使用它来保护Web表单免受CSFR攻击
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
#应用使用的数据库URL必须保存到Flask配置对象的SQLALCHEMY_DATABASE_URI键中
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 3
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT')or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL','false').lower() in ['true','on',1]
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # 设置分页常量
    POSTS_PER_PAGE = 3