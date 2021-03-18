from app import app
from flask import render_template, flash, redirect, url_for

#2个路由
from app.forms import LoginForm


@app.route('/',endpoint='index')
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

#使用URL的内部映射到视图函数来生成URL，以免每次修改需要全局搜索修改来重组链接
#定义登陆路由
@app.route('/loginyu',methods = ['GET','POST'])
def login():
    login_form = LoginForm() #表单实例化对象
    if login_form.validate_on_submit():
        msg = 'Login requested for user={},remember_me={}'.format(login_form.username.data,login_form.remember_me.data)
        flash(msg)
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign_In',form = login_form)





