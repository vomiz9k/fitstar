from app import app, db
import requests
from models import Excercise, MessageToExcercise, TrainerProfile, UserProfile
from difflib import SequenceMatcher
import os

YA_GPT_FOLDER_ID = os.environ.get('YA_GPT_FOLDER_ID')
YA_GPT_API_KEY = os.environ.get('YA_GPT_API_KEY')
YA_GPT_API_URL = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'


def gpt_request(messages):
    j = {
        "modelUri": f"gpt://{YA_GPT_FOLDER_ID}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6
        },
        "maxTokens": "1023",
        "messages": messages
    }

    response = requests.post(
        YA_GPT_API_URL,
        headers={
            "Authorization": f"Api-Key {YA_GPT_API_KEY}",
            "x-folder-id": YA_GPT_FOLDER_ID,
            "Content-Type": "Application/json"
        },
        json=j
    )

    text = response.json()['result']['alternatives'][0]['message']['text']

    return text

def get_about_me_message(profile):
    return (
        (f'Меня зовут {profile.name}. ' if profile.name else '') +
        (f'Мой пол: {profile.gender}. ' if profile.gender else '') +
        (f'Мой возраст: {profile.age}. ' if profile.age else '') +
        (f'Мой вес: {profile.weight}. ' if profile.weight else '') +
        (f'Мой рост: {profile.height}. ' if profile.height else '') +
        (f'Моя цель: {profile.goal}. ' if profile.goal else '')
    )


def get_recommended_trainer_id(user_id):
    trainer_profiles = db.session.query(TrainerProfile).all()
    trainers_msg = 'Тренеры: '

    for profile in trainer_profiles:
        trainers_msg += ( '{' +
            (f'Id: {profile.user_id}. ' if profile.id else '') +
            (f'Возраст: {profile.age}. ' if profile.age else '') +
            (f'Пол: {profile.gender}. ' if profile.gender else '') +
            (f'Вес: {profile.weight} кг. ' if profile.weight else '') +
            (f'Рост: {profile.height} см. ' if profile.height else '') +
            (f'Опыт: {profile.experience} лет. ' if profile.experience else '') +
            (f'Виды спорта: {",".join(profile.sports)}. ' if profile.sports else '') +
            (f'Теги: {",".join(profile.tags)}. ' if profile.tags else '') +
            (f'О себе: {profile.about}. ' if profile.about else '') + '},'
        )
    trainers_msg = trainers_msg[:-1]
    start_msg = 'Сейчас я тебе дам информацию о себе и информацию о тренерах. Тебе нужно выбрать среди них наиболее подходящего. Ответь только числом (Id тренера), не используй букв, не используй знаки препинания.'

    messages = [start_msg, trainers_msg]

    my_profile = db.session.query(UserProfile).filter(UserProfile.user_id == user_id).one_or_none()

    if my_profile:
        about_me_msg = 'Обо мне: ' + get_about_me_message(my_profile)
        messages.append(about_me_msg)

    messages_json = [
        {
            'role': 'system',
            'text': message
        } for message in messages
    ]

    text = gpt_request(messages_json)
    app.logger.error(text)

    return text




def find_revelant_excercises(text):
    excercises = db.session.query(Excercise.id, Excercise.name).all()

    scores = []
    for excercise in excercises:
        match = SequenceMatcher(None, text.lower().replace('ё', 'е'), excercise.name.lower().replace('ё', 'е')).find_longest_match()
        score = match.size / len(excercise.name)
        scores.append((score, excercise.id))

    scores = sorted(scores, key=lambda x: x[0])[::-1]
    scores = list(filter(lambda x: x[0] > 0.8, scores))[:5]

    app.logger.error(f"Filtered scores: {scores}")

    return [s[1] for s in scores]

def add_revelant_excercises(text, message_id):
    excercise_ids = find_revelant_excercises(text)
    for excercise_id in excercise_ids:
        msg_to_exc = MessageToExcercise(excercise_id=excercise_id, message_id=message_id)
        db.session.add(msg_to_exc)

    db.session.commit()