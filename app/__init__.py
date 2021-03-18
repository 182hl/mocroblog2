from flask import Flask
from config import Config
#
app = Flask(__name__)
#读取配置文件
app.config.from_object(Config)
print(app.config['SECRET_KEY'])

print("等会调用我", __name__)



from app import routs #从app包中导入模块routs

