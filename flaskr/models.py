from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from .database import Base
import datetime


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.now)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='posts')

    def __repr__(self):
        return '<Post(id={}, author={})>'.format(self.id, self.author.username)


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship('Post', order_by=Post.id, back_populates='author')

    def __repr__(self):
        return '<User(username={})>'.format(self.username)
