#encoding: utf-8

from exts import db
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
import datetime

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    username = db.Column(db.String(100),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)
    _password = db.Column(db.String(100),nullable=False)

    def __init__(self,*args,**kwargs):
        password = kwargs.pop('password')
        username = kwargs.pop('username')
        telephone = kwargs.pop('telephone')
        self.password = password
        self.username = username
        self.telephone = telephone

    @property # 把一个方法变成属性调用
    def password(self): # 外部使用
        return self._password

    @password.setter # 把一个setter方法变成属性赋值
    def password(self,rawpwd): # generate_password_hash是一个密码加盐哈希函数，生成的哈希值可通过 check_password_hash()进行验证
        self._password = generate_password_hash(rawpwd)

    def check_password(self,rawpwd):
        return check_password_hash(self._password,rawpwd)


class QuestionModel(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    # now()获取的是服务器第一次运行的时间
    # now就是每次创建一个模型的时候，都获取当前的时间
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    author_id = db.Column(db.String(100),db.ForeignKey('users.id'))

    author = db.relationship('UserModel',backref='questions') # 每个用户有多个问题

    __mapper_args__ = {
        'order_by': create_time.desc() # 按发布时间降序排列
    }

class AnswerModel(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey('questions.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('users.id'))

    # 每个问题有多个回答
    question = db.relationship('QuestionModel',backref=db.backref('answers',order_by=create_time.desc()))
    author = db.relationship('UserModel',backref='answers') # 每个用户有多个回答