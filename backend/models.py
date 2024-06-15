from app import db

from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    type = db.Column(db.String(80), nullable=False, server_default='user')


class UserProfile(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    name = db.Column(db.String(80), nullable=True)
    gender = db.Column(db.String(80), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    goal = db.Column(db.String(1024), nullable=True)


class TrainerProfile(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    name = db.Column(db.String(80), nullable=True)
    gender = db.Column(db.String(80), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    sports = db.Column(ARRAY(db.String(80)), nullable=True)
    tags = db.Column(ARRAY(db.String(80)), nullable=True)
    about = db.Column(db.String(1024), nullable=True)


class TrainerReview(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    trainer_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    author_user_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    mark = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(4096), nullable=True)

    _table_args__ = (
        db.UniqueConstraint('trainer_user_id', 'author_user_id'),
    )


class Workout(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    trainer_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    name = db.Column(db.String(1024), nullable=True)
    description = db.Column(db.String(4096), nullable=True)
    zoom_link = db.Column(db.String(4096), nullable=True)
    time_start = db.Column(db.Integer(), nullable=False, index=True)
    time_finish = db.Column(db.Integer(), nullable=False, index=True)

class Excercise(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096), nullable=False, unique=True)
    muscles = db.Column(ARRAY(db.String(80)), nullable=True)
    type = db.Column(db.String(80), nullable=True)
    equipment = db.Column(ARRAY(db.String(80)), nullable=True)
    difficulty = db.Column(db.String(80), nullable=True)


class ExcerciseToImage(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    excercise_id = db.Column(db.Integer, db.ForeignKey('excercise.id'), nullable=False, index=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)

    _table_args__ = (
        db.UniqueConstraint('excercise_id', 'image_id'),
    )


class MessageToExcercise(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False, index=True)
    excercise_id = db.Column(db.Integer, db.ForeignKey('excercise.id'), nullable=False, index=True)


class Chat(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)


class UserToChat(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    _table_args__ = (
        db.UniqueConstraint('chat_id', 'user_id'),
    )


class Message(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False, index=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    time = db.Column(db.Integer(), nullable=True, index=True)
    text = db.Column(db.String(4096), nullable=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)


class Image(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(1024), nullable=False, unique=True)
    url = db.Column(db.String(1024), nullable=False)


class Achievment(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(1024), nullable=False)


class UserAchievments(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    achievment_id = db.Column(db.Integer, db.ForeignKey('achievment.id'), nullable=False, index=True)
