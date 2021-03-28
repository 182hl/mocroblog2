from datetime import datetime,timedelta
import unittest
from app import db, app
from app.model import User,Post


class UserModelCase(unittest.TestCase):
    #在执行测试方法之前执行一次setUp方法
    def setUp(self):
        #设置内存数据库
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    #在执行测试方法之后执行一次tearDown方法
    def tearDown(self):
        db.session.remove()
        #清空数据库
        db.drop_all()

    #测试hashing密码方法，单元测试方法以test_下划线开头
    def test_password_hashing(self):
        u = User(username='susan2018')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    #测试生成的邮箱地址相不相等
    def test_avatar(self):
        u = User(username='john',email='john@example.com')
        self.assertEqual(u.avatar(128),('https://www.gravatar.com/avatar'
                                        '/d4c74594d841139328695756648b6bd6'
                                        '?d=identicon&s=128'))
    #测试关注和被关注
    def test_follow(self):
        u1 = User(username='john',email='john@example.com')
        u2 = User(username='susan',email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(),[])
        self.assertEqual(u2.followers.all(),[])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(),1)
        self.assertEqual(u1.followed.first().username,'susan')
        self.assertEqual(u2.followers.count(),1)
        self.assertEqual(u2.followers.first().username,'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(),0)
        self.assertEqual(u2.followers.count(),0)

    def test_follow_posts(self):
        #create for users
        u1 = User(username='john',email='john@example.com')
        u2 = User(username='susan',email='susan@example.com')
        u3 = User(username='mary',email='mary@example.com')
        u4 = User(username='david',email='davied@example.com')
        db.session.add_all([u1,u2,u3,u4])


        #create for posts
        now = datetime.utcnow()
        p1 = Post(body="post from john",author=u1,timestamp=now+timedelta(seconds=1))
        p2 = Post(body="post from susan",author=u2,timestamp=now+timedelta(seconds=2))
        p3 = Post(body="post from mary",author=u3,timestamp=now+timedelta(seconds=3))
        p4 = Post(body="post from davied",author=u4,timestamp=now+timedelta(seconds=4))
        db.session.add_all([p1,p2,p3,p4])
        db.session.commit()

        #setup for followers
        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()

        self.assertEqual(f1,[p4,p2,p1])
        self.assertEqual(f2,[p3,p2])
        self.assertEqual(f3,[p4,p3])
        self.assertEqual(f4,[p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)