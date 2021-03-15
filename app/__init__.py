from flask import Flask

#
app = Flask(__name__)


print("等会调用我", __name__)

from app import routs #从app包中导入模块routs
