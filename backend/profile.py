import json
from werkzeug import exceptions
from app import app, db
from models import User, TrainerProfile, UserProfile, Image
from ai_trainer import AI_TRAINER_USER_ID
from flask import request
from ai_trainer import AI_TRAINER_USER_ID
import util


USER_FIELDS = ["image_id", "username"]

@app.route('/users/<int:user_id>/profile', methods=['POST'])
def update_profile(user_id):
    j = request.get_json()

    app.logger.error(f'{j}')

    user_data = {k: j[k] for k in j if k in USER_FIELDS}
    profile_data = {k: j[k] for k in j if k not in USER_FIELDS}

    if user_data:
        db.session.query(User).filter(User.id == user_id).update(user_data)
        db.session.flush()

    user = db.session.query(User).filter(User.id == user_id).one_or_none()

    if not user:
        raise exceptions.NotFound("user not found")

    if profile_data:
        if user.type == 'trainer':
            db.session.query(TrainerProfile).filter(TrainerProfile.user_id == user_id).update(profile_data)
            db.session.flush()

            trainer_profile = db.session.query(TrainerProfile).filter(TrainerProfile.user_id == user_id).one_or_none()
            if not trainer_profile:
                trainer_profile = TrainerProfile(**profile_data, user_id=user_id)
                db.session.add(trainer_profile)

        if user.type == 'user':
            db.session.query(UserProfile).filter(UserProfile.user_id == user_id).update(profile_data)
            db.session.flush()

            user_profile = db.session.query(UserProfile).filter(UserProfile.user_id == user_id).one_or_none()
            if not user_profile:
                user_profile = UserProfile(**profile_data, user_id=user_id)
                db.session.add(user_profile)


    db.session.commit()

    return {'id' : user_id}

@app.route('/users/<int:user_id>/profile', methods=['GET'])
def get_profile(user_id):

    user = db.session.query(
        User.username, User.id, Image.url.label('image'), User.type
    ).join(
        Image, User.image_id == Image.id, isouter=True
    ).filter(
        User.id == user_id
    ).one_or_none()

    profile = None
    if not user:
        raise exceptions.NotFound("user not found")

    if user.type == 'trainer':
        profile = db.session.query(TrainerProfile).filter(TrainerProfile.user_id == user_id).one_or_none()

    if user.type == 'user':
        profile = db.session.query(UserProfile).filter(UserProfile.user_id == user_id).one_or_none()

    return {'user': user._asdict(), 'profile': profile.to_dict() if profile else None}


@app.route('/users/<int:user_id>/trainers', methods=['GET'])
def trainers(user_id):
    users = db.session.query(
        User.username, User.id, Image.url.label('image'), User.type
    ).join(
        Image, User.image_id == Image.id, isouter=True
    ).filter(
        User.type == 'trainer', User.id != AI_TRAINER_USER_ID
    ).order_by(
        User.id
    ).all()

    recommended_trainer_id = int(util.get_recommended_trainer_id(user_id))

    result = []

    for user in users:
        profile = db.session.query(TrainerProfile).filter(TrainerProfile.user_id == user.id).one_or_none()
        result.append({
            'user': user._asdict(),
            'profile': profile.to_dict() if profile else None,
            'is_recomended': recommended_trainer_id == user.id
        })

    return result