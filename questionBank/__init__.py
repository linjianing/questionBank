from flask import Flask
import os
import sys

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from questionBank.converters import DictConverter

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', default='dev')   # used for flask-wtf to avoid csrf attack

# 配置自动转换器
app.url_map.converters['dict'] = DictConverter

# 文件上传路径
app.config['UPLOADED_PATH'] = 'uploads'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from questionBank import views, commands

