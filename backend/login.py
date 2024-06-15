import json
from werkzeug import exceptions
from app import app, db
from models import User, Chat, UserToChat
from ai_trainer import AI_TRAINER_USER_ID
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from flask import Flask, jsonify
from flask import Flask, render_template, request, redirect, session


@app.route('/login', methods=['POST'])
def login():
    j = request.get_json()
    username = j['username']
    password = j['password']
    user_type = j.get('type', 'trainee')

    user = db.session.query(User).filter(User.username==username).one_or_none()
    if user is None:
        new_user = User(username=username, password=password)
        db.session.add(new_user)

        chat_with_ai = Chat()
        db.session.add(chat_with_ai)
        db.session.flush()

        user_to_chat_self = UserToChat(user_id=new_user.id, chat_id=chat_with_ai.id)
        user_to_chat_ai = UserToChat(user_id=AI_TRAINER_USER_ID, chat_id=chat_with_ai.id)

        db.session.add(user_to_chat_ai)
        db.session.add(user_to_chat_self)

        db.session.commit()
        return {'id': new_user.id}
    else:
        if user.password == password:
            return {'id': user.id}
        else:
            raise exceptions.Forbidden("invalid password")







