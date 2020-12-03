from flask import Flask
import os
import sys

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', default='dev')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from questionBank import views, commands