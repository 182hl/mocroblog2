from app import app
from flask import render_template

#2个路由
@app.route('/')
@app.route('/index')

#1个视图函数
def index():
    user = {"username": "Migeal"}
    # return "hello,World" #返回一个字符串

    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',user=user,posts=posts)





