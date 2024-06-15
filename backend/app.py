from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{os.environ.get("POSTGRESQL_PASSWORD")}@fit_postgres_1:5432/postgres'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

from models import *
from handlers import *
from upload import configure_fu

photos = configure_fu()

if __name__ == '__main__':
    app.run()