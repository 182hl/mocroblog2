from flask import Flask, request, current_app
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment

from config import Config
from flask_sqlalchemy import SQLAlchemy

from flask_bootstrap import Bootstrap

from flask_mail import Mail
from flask_babel import Babel,lazy_gettext as _l
#
#app = Flask(__name__)
#读取配置文件
#app.config.from_object(Config)
#print(app.config['SECRET_KEY'])


db = SQLAlchemy() #数据库迁移对象

mail = Mail()
bootstrap = Bootstrap()
migrate = Migrate()  #迁移引擎对象
moment = Moment()
babel = Babel()

#处理随客户端请求发送的Accept-Language headers，这个header将客户端语言和区域设置首选指定为加权列表
#可在浏览器的首选项页面中配置这个标题下header的内容
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])



login = LoginManager()
#如果没有登陆的话登陆到这个页面
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
print("等会调用我", __name__)


def create_app(config_class):
    #将Flask类的实例赋值给名为app的变量，这个实例成为app包的成员
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)


    #注册蓝图
    # from app.errors import bp as errors_bp
    # app.register_blueprint(errors_bp)


    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    #
    # if not app.debug:
    #     if not os.path.exits('login'):
    #         os.mkdir('logs')
    #     file_handler = RotatingFileHandler('logs/microblog.log',maxBytes=10240,backupCount=10)
    #
    #     file_handler.setFormatter(logging.Formatter(
    #         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    #     file_handler.setLevel(logging.INFO)
    #     app.logger.addHandler(file_handler)
    #
    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('Microblog startup')

    return app


from app import model #从app包中导入模块routs,model


