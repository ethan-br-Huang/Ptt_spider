from flask_login import UserMixin
from . import db


class userTB(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True, index=True)
    password_salt = db.Column(db.Text(), nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)

    def get_id(self):
        return self.id


class pictureTB(db.Model):
    __tablename__ = 'Picture'
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    author_id = db.Column(db.Integer(), db.ForeignKey('User.id'), nullable=False)
    data = db.Column(db.Text(), nullable=False)
