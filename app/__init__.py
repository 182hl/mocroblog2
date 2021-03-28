import login as login
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail
#
app = Flask(__name__)
#读取配置文件
app.config.from_object(Config)
print(app.config['SECRET_KEY'])


db = SQLAlchemy(app) #数据库迁移对象
#如果没有登陆的话登陆到这个页面
login.login_view = 'login'
mail = Mail(app)
migrate = Migrate(app,db)  #迁移引擎对象


login = LoginManager(app)
print("等会调用我", __name__)



from app import routs,model #从app包中导入模块routs,model


