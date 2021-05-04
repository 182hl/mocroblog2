from flask_login import logout_user
from flask_babel import _

from app import db
from app.auth import bp
from flask import render_template, flash, redirect, url_for

#2个路由
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ReserPasswordForm
from flask_login import current_user,login_user
from app.model import User
from app.auth.email import send_password_reset_email



#重置密码功能
@bp.route('/reset_password_request',methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))


    return render_template('email/reset_password_request.html',title='Reset Password',form=form)

@bp.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    #查看当前用户是否已登录，如果是已登录状态，则返回主页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    #根据token校验用户的id是否在数据库里存在
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ReserPasswordForm()
    #如果提交了新密码，则更新新密码
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html',form=form)



#使用URL的内部映射到视图函数来生成URL，以免每次修改需要全局搜索修改来重组链接
#定义登陆路由
@bp.route('/loginyu',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    login_form = LoginForm() #表单实例化对象
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash(_('invalid usename or password'))
        #添加用户信息到session
        login_user(user,login_form.remember_me.data)

        #点击登陆之后自动跳转到指定的下一页
        # next_page = request.args.get('next')
        # print(url_parse(next_page).netloc)
        # if not next_page or url_parse(next_page).netloc!='':
        #     next_page = url_for('index')
        # return redirect(next_page)

    #     flash(msg)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html',title='Sign_In',form = login_form)

#退出功能
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

#注册功能
@bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Configulations, you sre now a regesterred user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',title='Register',form=form)