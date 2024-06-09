from app import db

from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(1024), nullable=True, server_default='https://hb.bizmrg.com/st.cityfootball.ru/player/147521/photo/6330540f23d81_295x295.jpg')


# class Trainer(db.Model, SerializerMixin):
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)


# class Trainee(db.Model, SerializerMixin):
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
#     age = db.Column(db.Integer, nullable=False)
#     male = db.Column(db.Boolean, nullable=False)
#     weight = db.Column(db.Integer, nullable=True)
#     height = db.Column(db.Integer, nullable=True)
#     goal = db.Column(db.String(1024), nullable=True)

difficulties = ['']

class Excercise(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), nullable=True)
    description = db.Column(db.String(1024), nullable=True)
    muscle = db.Column(db.String(1024), nullable=True)

class ExcerciseToPhoto(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    excercise_id = db.Column(db.Integer, db.ForeignKey('excercise.id'), nullable=False, index=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)

class Chat(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)

class UserToChat(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

class Message(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False, index=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    time = db.Column(db.Integer(), nullable=True, index=True)
    text = db.Column(db.String(1024), nullable=True)
    image = db.Column(db.String(1024), nullable=True)

class Image(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(1024), nullable=False)

