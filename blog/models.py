from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from blog import db
from werkzeug.security import generate_password_hash, check_password_hash
from blog import login_manager
from flask_login import UserMixin
from markdown import markdown
import bleach

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable = False)
    username = db.Column(db.String(), nullable = False, unique = True)
    password_hash = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False, unique = True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)


class BlogPost(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(length = 50), nullable = False, unique = True)
    subtitle = db.Column(db.String(length = 50), nullable = False, unique = True)
    back_image_name = db.Column(db.String(length = 50), unique = True, nullable = False)
    image_name = db.Column(db.String(length = 50), unique = True, nullable = False)
    body = db.Column(db.String(), nullable = False)
    date = db.Column(db.String())
    body_html = db.Column(db.Text)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
            'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
        tags=allowed_tags, strip=True))
    comment = db.relationship('Comment', backref = 'comment', lazy = True)

db.event.listen(BlogPost.body, 'set', BlogPost.on_changed_body)



class Portfolio(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(length = 40), nullable = False, unique = True)
    link = db.Column(db.String(), nullable = True)
    github = db.Column(db.String(), nullable = False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(length = 200), nullable = False)
    date = db.Column(db.String())
    body = db.Column(db.String(length = 200), nullable = False)
    owner = db.Column(db.Integer(), db.ForeignKey('blog.id'))