import time
from app import db, app

import util
from models import Message, UserProfile, MessageToExcercise

AI_TRAINER_USER_ID = 1

def default_messages(user_id):
    result = [
        {
            "role": "system",
            "text": """
            Ты фитнес-тренер.
             Разговаривай со мной как обычный человек, не выдавай, что ты искуственный интеллект.
             Не говори про консультацию с врачом.
            """
        }
    ]
    profile = db.session.query(UserProfile).filter(UserProfile.user_id == user_id).one_or_none()

    if not profile:
        return result

    s = util.get_about_me_message(profile)

    result.append({
        'role': 'system',
        'text': s
    })
    return result

def answer(user_id, chat_id):
    last_messages = db.session.query(Message).filter(Message.chat_id == chat_id).order_by(Message.id.desc()).limit(10).all()[::-1]

    last_messages = [
        {
            "role": "assistant" if message.sender == AI_TRAINER_USER_ID else "user",
            "text": message.text
        }
        for message in last_messages
    ]

    messages = default_messages(user_id) + last_messages

    text = util.gpt_request(messages)

    new_message = Message(sender=AI_TRAINER_USER_ID, chat_id=chat_id, time=time.time(), text=text)
    db.session.add(new_message)
    db.session.flush()

    excercise_ids = util.find_revelant_excercises(text)
    for excercise_id in excercise_ids:
        msg_to_exc = MessageToExcercise(excercise_id=excercise_id, message_id=new_message.id)
        db.session.add(msg_to_exc)

    db.session.commit()


def process_ai_trainer(user_id, chat_id):
    answer(user_id, chat_id),

