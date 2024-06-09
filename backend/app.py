import json

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate
from flask import Flask, jsonify
from flask import request, Response


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@fit_postgres_1:5432/postgres'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

from models import *
from login import login
from upload import upload, show

@app.route('/users/<int:user_id>/chats', methods=['GET'])
def chats(user_id):
    user_to_chats = db.session.query(UserToChat).filter(UserToChat.user_id == user_id).all()
    result = []
    for user_to_chat in user_to_chats:
        messages = db.session.query(Message.id, Message.sender, Message.time, Message.text, Message.image).filter(Message.chat_id == user_to_chat.chat_id).order_by(Message.time).all()
        user = db.session.query(User.username, User.id, User.image).join(UserToChat, User.id == UserToChat.user_id).filter(UserToChat.chat_id == user_to_chat.chat_id, User.id != user_id).one()
        result.append({
            'chat': user_to_chat.chat_id,
            'user': user._asdict(),
            'messages': [m._asdict() for m in messages]
        })

    result = sorted(result, key=lambda x: x['messages'][-1]['time'] if x['messages'] else 0)

    return result


@app.route('/send-message', methods=['POST'])
def send_message():
    j = request.get_json()
    user_id = j['user_id']
    chat_id = j['chat_id']
    time = j['time']
    text = j.get('text')
    image = j.get('image')

    message = Message(chat_id=chat_id, sender=user_id, time=time, text=text, image=image)
    db.session.add(message)
    db.session.commit()

    return {'id': message.id}

@app.route('/new-chat', methods=['POST'])
def new_chat():
    j = request.get_json()
    users = j['users']
    chat = Chat()
    db.session.add(chat)
    db.session.flush()

    for user in users:
        user_to_chat = UserToChat(chat_id=chat.id, user_id=user)
        db.session.add(user_to_chat)

    db.session.commit()
    return {'id': chat.id}


if __name__ == '__main__':
    app.run()