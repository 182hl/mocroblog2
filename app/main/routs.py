from datetime import datetime

from flask_login import login_required
from guess_language import guess_language
from flask_babel import _

from app import db
from app.main import bp
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app

#2个路由
from app.main.forms import EditProfileForm, PostForm
from flask_login import current_user
from app.model import User, Post

from app.translate import translate


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/',endpoint='index',methods = ['GET','POST'])
@bp.route('/index',methods = ['GET','POST'])
#必须登陆才能访问的页面，做登录校验
@login_required
#1个视图函数
def index():
    # user = {"username": "Migeal"}
    # # return "hello,World" #返回一个字符串
    #提交博客方法
    form =PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ' '
        post = Post(body=form.post.data,author=current_user,language=language)
        db.session.add(post)
        db.session.commit()
        #_()函数将文本包装在基本语言中
        flash(_('Your post is now live!'))
        #重定向的好处是刷新页面的时候不会把之前的表单内容再请求一次
        return redirect(url_for('main.index'))

    # if current_user.is_authenticated:
    # 加载用户提交过的博客内容
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',title = 'Home Page',posts = posts.items,form=form,next_url=next_url,prev_url=prev_url)
    # posts = [
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }]
    return render_template('index.html',title = 'Home',posts = posts)




#用户个人资料的视图函数
@bp.route('/user/<username>')
#需要登陆才有权限访问的页面
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = [
    #     {'author':user, 'body': 'Test post #1'},
    #     {'author':user, 'body': 'Test post #2'}
    # ]
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user',username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user = user, posts = posts.items,next_url=next_url,prev_url=prev_url)


#编辑用户信息
@bp.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title='Edit Profile',form=form)


#关注功能
@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot folllow yourself!')
        return redirect(url_for('user',username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %{username}!',username=username))
    return redirect(url_for('main.user',username=username))


#取消关注功能
@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user',username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user',username=username))



#浏览所有用户的帖子
@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',title='Explore',posts=posts.items,next_url=next_url,prev_url=prev_url)


@bp.route('/translate',methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text':translate(request.form['text'],request.form['source_language'],request.form['dest_language'])})

