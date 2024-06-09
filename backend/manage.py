import os


from app import app, db, manager
from flask_migrate import MigrateCommand


app.config.from_object(os.environ['APP_SETTINGS'])

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()