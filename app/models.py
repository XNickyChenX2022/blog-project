from sqlalchemy.orm import backref
from .extensions import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Index, text, cast, literal
from sqlalchemy.dialects.postgresql import REGCONFIG, TSVECTOR
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.types import TypeDecorator

class TSVector(TypeDecorator):
    impl = TSVECTOR
    cache_ok = True
    
def to_tsvector_ix(*columns):
    s = " || ' ' || ".join(columns)
    return func.to_tsvector(cast(literal('english'), type_=REGCONFIG), text(s))

# 0 means that it is not liked, 1 means it is likes, 2 means disliked for mode
class UserPost(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    mode = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship('Users', back_populates='user_post')
    post = db.relationship('Posts', back_populates='user_post')

class UserComment(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),  primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'),  primary_key=True)
    mode = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship('Users', back_populates='user_comment')
    comment = db.relationship('Comments', back_populates='user_comment')
    
    # def change_mode(mode):
    def __repr__(self):
        return '<User %r Comment %r >' %(self.user_id, self.comment_id)    

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    posts_id = db.relationship('Posts', backref='user')
    comment_id = db.relationship('Comments', backref='user')
    user_comment = db.relationship('UserComment', back_populates='user')
    user_post = db.relationship('UserPost', back_populates='user')
    
    def __repr__(self):
        return '<Users %r>' % self.id

# chnage to text
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comments', backref='post')
    user_post = db.relationship('UserPost', back_populates='post')
    
    
    ts_vector = db.Column(TSVector(), db.Computed(
         "to_tsvector('english', title || ' ' || text)",
         persisted=True))
    
    __table_args__ = (
        Index(
            'ts_vector',
            to_tsvector_ix('title', 'text'),
            postgresql_using='gin'
        ),
    )
    
    def __repr__(self):
        return '<Posts %r>' % self.id


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer,  db.ForeignKey('users.id'), nullable=False)
    replies = db.relationship('Comments', cascade='delete', backref=backref('parent', remote_side=[id]), lazy='dynamic')
    user_comment = db.relationship('UserComment', cascade='delete, all', back_populates='comment')

    def __repr__(self):
        return '<Comments %r>' % self.id
