from werkzeug import exceptions
from app import app, db
from models import Excercise, ExcerciseToImage, Image
from flask import request



@app.route('/excercise', methods=['POST'])
def new_excercise():
    j = request.get_json()

    name = j['name']
    muscles = j.get('muscles', [])
    type = j.get('type')
    equipment = j.get('equipment', [])
    difficulty = j.get('difficulty')

    excercise = Excercise(
        name=name,
        muscles=muscles,
        type=type,
        equipment=equipment,
        difficulty=difficulty
    )

    db.session.add(excercise)
    db.session.flush()

    for image_id in j.get('image_ids', []):
        exc_to_img = ExcerciseToImage(excercise_id=excercise.id, image_id=image_id)
        db.session.add(exc_to_img)

    db.session.commit()

    return {'id' : excercise.id}

@app.route('/excercises', methods=['GET'])
def get_excercises():
    excs = db.session.query(Excercise).all()
    result = []

    for exc in excs:
        images = db.session.query(Image.url).join(
            ExcerciseToImage, Image.id == ExcerciseToImage.image_id
        ).filter(
            ExcerciseToImage.excercise_id == exc.id
        ).all()

        result.append(
            exc.to_dict() | {'images': [i[0] for i in images]}
        )

    return result

@app.route('/excercises/<int:excercise_id>', methods=['GET'])
def get_excercise(excercise_id):
    exc = db.session.query(Excercise).filter(Excercise.id == excercise_id).one_or_none()

    images = db.session.query(Image.url).join(
        ExcerciseToImage, Image.id == ExcerciseToImage.image_id
    ).filter(
        ExcerciseToImage.excercise_id == exc.id
    ).all()

    if exc:
        return exc.to_dict() | {'images': [i[0] for i in images]}

    raise exceptions.NotFound("Excercise not found")