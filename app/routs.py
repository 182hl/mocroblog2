from app import app

#2个路由
@app.route('/')
@app.route('/index')

#1个视图函数
def index():
    return "hello,World" #返回一个字符串