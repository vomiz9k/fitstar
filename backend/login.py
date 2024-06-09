import json
from werkzeug import exceptions
from app import app, db
from models import User
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

    user = db.session.query(User).filter(User.username==username).one_or_none()
    if user is None:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'id': new_user.id}
    else:
        if user.password == password:
            return {'id': user.id}
        else:
            raise exceptions.Forbidden("invalid password")







