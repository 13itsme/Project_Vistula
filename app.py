import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# === Настройки приложения ===
app = Flask(__name__) # Создание экземпляра приложения Flask.

# Создание instance и абсолютного пути для базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'app.db')
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "super_secret_key") # Устанавливает секретный ключ для Flask-приложения.
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}' # Подключение базы к Flask и установка пути
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы
db = SQLAlchemy(app)
migrate = Migrate(app, db) # Объект для управления миграциям БД

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
