import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

# === Настройки приложения ===
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'app.db')
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)  # создаёт папку, если нет

app.config['SECRET_KEY'] = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# === Инициализация ===
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Session(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
