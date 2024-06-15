from app import app, db
from models import User, Workout

from flask import request



@app.route('/users/<int:user_id>/workouts', methods=['GET'])
def get_workouts(user_id):
    user = db.session.query(User).filter(User.id == user_id).one()

    if user.type == 'user':
        workouts = db.session.query(Workout).filter(Workout.user_id == user_id).all()
    else:
        workouts = db.session.query(Workout).filter(Workout.trainer_user_id == user_id).all()

    return [w.to_dict() for w in workouts]


@app.route('/new-workout', methods=['POST'])
def new_workout():
    j = request.get_json()
    app.logger.error(f'{j}')
    trainer_user_id = j['trainer_user_id']

    time_start = j['time_start']
    time_finish = j['time_finish']

    name = j.get('name')
    user_id = j.get('user_id')
    description = j.get('description')

    workout = Workout(
        trainer_user_id=trainer_user_id,
        name=name,
        time_start=time_start,
        time_finish=time_finish,
        user_id=user_id,
        description=description,
    #    zoom_link=TODO
    )

    db.session.add(workout)
    db.session.commit()


    return {'id': workout.id}

@app.route('/submit-workout', methods=['POST'])
def submit_workout():
    j = request.get_json()

    name = j.get('name')
    user_id = j['user_id']
    workout_id = j['workout_id']

    workout = db.session.query(Workout).filter(Workout.id == workout_id).one()
    workout.user_id = user_id
    if name:
        workout.name = name
    db.session.commit()

    return {'id': workout.id}
