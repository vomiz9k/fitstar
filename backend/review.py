import json
from werkzeug import exceptions
from app import app, db
from models import TrainerReview
from ai_trainer import AI_TRAINER_USER_ID
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from flask import Flask, jsonify
from flask import Flask, render_template, request


@app.route('/review', methods=['POST'])
def new_review():
    j = request.get_json()
    app.logger.error(f'json: {j}')

    author_user_id = j['author_user_id']
    trainer_user_id = j['trainer_user_id']
    mark = j['mark']
    text = j.get('text')

    review = TrainerReview(author_user_id=author_user_id, trainer_user_id=trainer_user_id, mark=mark, text=text)
    db.session.add(review)
    db.session.commit()

    return {'id' : review.id}

@app.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_reviews(user_id):
    reviews = db.session.query(TrainerReview).filter(TrainerReview.trainer_user_id == user_id).all()

    return [r.to_dict() for r in reviews]