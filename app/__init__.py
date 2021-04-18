import login as login
from flask import Flask, request
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_babel import Babel

from config import Config
from flask_sqlalchemy import SQLAlchemy

from flask_bootstrap import Bootstrap

from flask_mail import Mail
from flask_babel import Babel,lazy_gettext as _l
#
app = Flask(__name__)
#读取配置文件
app.config.from_object(Config)
print(app.config['SECRET_KEY'])


db = SQLAlchemy(app) #数据库迁移对象

mail = Mail(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app,db)  #迁移引擎对象
moment = Moment(app)
babel = Babel(app)

#处理随客户端请求发送的Accept-Language headers，这个header将客户端语言和区域设置首选指定为加权列表
#可在浏览器的首选项页面中配置这个标题下header的内容
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


login = LoginManager(app)
#如果没有登陆的话登陆到这个页面
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
print("等会调用我", __name__)



from app import routs,model #从app包中导入模块routs,model


