from datetime import datetime

import remember as remember
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import form
from werkzeug.urls import url_parse

from app import app, db
from flask import render_template, flash, redirect, url_for, request

#2个路由
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user,login_user
from app.model import User

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/',endpoint='index')
@app.route('/index')
#必须登陆才能访问的页面，做登录校验
# @login_required
#1个视图函数
def index():
    # user = {"username": "Migeal"}
    # # return "hello,World" #返回一个字符串
    #
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
    return render_template('index.html',title = 'Home',posts=posts)

#使用URL的内部映射到视图函数来生成URL，以免每次修改需要全局搜索修改来重组链接
#定义登陆路由
@app.route('/loginyu',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm() #表单实例化对象
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('invalid usename or password')
        #添加用户信息到session
        login_user(user,login_form.remember_me.data)

        #点击登陆之后自动跳转到指定的下一页
        # next_page = request.args.get('next')
        # print(url_parse(next_page).netloc)
        # if not next_page or url_parse(next_page).netloc!='':
        #     next_page = url_for('index')
        # return redirect(next_page)

    #     flash(msg)
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign_In',form = login_form)

#退出功能
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#注册功能
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Configulations, you sre now a regesterred user!')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)


#用户个人资料的视图函数
@app.route('/user/<username>')
#需要登陆才有权限访问的页面
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user, 'body': 'Test post #1'},
        {'author':user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user = user, posts = posts)


#编辑用户信息
@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title='Edit Profile',form=form)





