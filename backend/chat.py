from flask import request
import json

from sqlalchemy import func
from werkzeug import exceptions

from models import Chat, UserToChat, Message, Image, User, MessageToExcercise, UserProfile, TrainerProfile

import util
from ai_trainer import AI_TRAINER_USER_ID, process_ai_trainer

from app import app, db

@app.route('/users/<int:user_id>/chats', methods=['GET'])
def chats(user_id):
    user_to_chats = db.session.query(UserToChat).filter(UserToChat.user_id == user_id).all()
    result = []
    for user_to_chat in user_to_chats:

        messages = db.session.query(
            Message.id, Message.sender, Message.time, Message.text, Image.url.label('image')
        ).join(
            Image, Message.image_id == Image.id, isouter=True
        ).filter(
            Message.chat_id == user_to_chat.chat_id
        ).order_by(
            Message.id
        ).all()

        messages_json = []
        for message in messages:
            d = message._asdict()
            excs = db.session.query(MessageToExcercise.excercise_id).filter(MessageToExcercise.message_id == message.id).all()
            if excs:
                d['excercises'] = [e[0] for e in excs]
            messages_json.append(d)

        user = db.session.query(
            User.username, User.id, Image.url.label('image'), User.type
        ).join(
            UserToChat, User.id == UserToChat.user_id
        ).join(
            Image, User.image_id == Image.id, isouter=True
        ).filter(
            UserToChat.chat_id == user_to_chat.chat_id, User.id != user_id
        ).one()

        profile = None
        if user.type == 'user':
            profile = db.session.query(UserProfile).filter(UserProfile.user_id == user.id).one_or_none()
        else:
            profile = db.session.query(TrainerProfile).filter(TrainerProfile.user_id == user.id).one_or_none()

        result.append({
            'chat': user_to_chat.chat_id,
            'user': user._asdict() if user else None,
            'profile': profile.to_dict() if profile else None,
            'messages': messages_json
        })

    result = sorted(
        result,
        key=lambda x: 9132701921237912 if x['user'] == AI_TRAINER_USER_ID else x['messages'][-1]['id'] if x['messages'] else 0
    )

    return result


@app.route('/send-message', methods=['POST'])
def send_message():
    j = request.get_json()
    user_id = j['user_id']
    chat_id = j['chat_id']
    time = j['time']
    text = j.get('text')
    image_id = j.get('image_id')

    message = Message(chat_id=chat_id, sender=user_id, time=time, text=text, image_id=image_id)
    db.session.add(message)
    db.session.commit()

    sender = db.session.query(User).filter(User.id == user_id).one()
    if sender.type == 'trainer':
        util.add_revelant_excercises(message.text, message.id)

    receiver = db.session.query(User).join(
        UserToChat, UserToChat.user_id == User.id
    ).filter(User.id != user_id, UserToChat.chat_id == chat_id).one()

    if receiver.id == AI_TRAINER_USER_ID:
        process_ai_trainer(user_id, chat_id)

    return {'id': message.id}


@app.route('/new-chat', methods=['POST'])
def new_chat():
    j = request.get_json()
    users = j['users']

    chat_exists = db.session.query(func.count(Chat.id).label('cnt')).join(
        UserToChat, Chat.id == UserToChat.chat_id
    ).filter(
        UserToChat.user_id.in_(users)
    ).group_by(
        Chat.id
    ).having(
        func.count(Chat.id) == len(users)
    ).all()

    app.logger.error(' '.join(json.dumps(x._asdict()) for x in chat_exists))

    if chat_exists:
        raise exceptions.BadRequest("chat exists")

    chat = Chat()
    db.session.add(chat)
    db.session.flush()

    for user in users:
        user_to_chat = UserToChat(chat_id=chat.id, user_id=user)
        db.session.add(user_to_chat)

    db.session.commit()
    return {'id': chat.id}
