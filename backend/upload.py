import flask_uploads as fu
from werkzeug import exceptions
from flask import request
from models import Image
from app import db, app
from uuid import uuid4
import os

photos = None

def configure_fu():
    global photos

    app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config['UPLOADS_AUTOSERVE'] = True
    photos = fu.UploadSet('photos', fu.IMAGES)
    fu.configure_uploads(app, photos)
    return photos

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        filename = photos.save(request.files['image'], name=str(uuid4()) + '.')
        rec = Image(filename=filename, url=photos.url(filename))
        db.session.add(rec)
        db.session.commit()
        return {"id": rec.id, "url": rec.url}
    raise exceptions.BadRequest()


@app.route('/images/<id>', methods=['GET'])
def show(id):
    photo = db.session.query(Image.filename).filter(Image.id==id).one_or_none()
    if photo is None:
        raise exceptions.BadRequestKeyError("invalid image id")
    url = photos.url(photo.filename)
    return {"img_url": url}