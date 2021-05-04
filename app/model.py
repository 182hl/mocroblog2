from datetime import datetime
from time import time

import algorithm as algorithm
import jwt
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
#混用类
from flask_login import UserMixin
from app import login

from hashlib import md5

#加载用户信息使用
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


followers = db.Table(
    'followers',
    db.Column('follower_id',db.Integer,db.ForeignKey('user.id')), #关注你的人的id
    db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))  #你关注的人的id
)


#继承UserMixin类属性
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index = True, unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)

    #博主和关注者的联系
    followed = db.relationship(
        'User',
        secondary = followers,
        primaryjoin = (followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref('followers',lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    #结合自己和关注者的帖子
    def followed_posts(self):
        followed = Post.query.join(followers,(followers.c.followed_id==Post.user_id)).filter(followers.c.follower_id==self.id)
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    #添加和删除用户
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0

    #获取已关注用户的所有帖子,采用sqlalchemy查询方法
    # def followed_posts1(self):
    #     #帖子表里的被关注的人发的所有的帖子里面过滤出关注者是本身的帖子
    #     return Post.query.join(
    #         followers,(followers.c.followed_id==Post.user_id)).filter(
    #         followers.c.follower_id==self.id).order_by(
    #             Post.timestamp.desc())



    #以字符串形式生成一个JWT令牌
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'],
                          algorithm='HS256').encode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

#alchemy 使用sql语句进行查询
#sql = """sql语句""""
#list_top=db.session.execute(sql).fetchall()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 提交帖子时输入的语言，语言自动被识别存入数据库
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

