### 📘 Description
This is a simple web application built with **Flask** and **SQLite**, designed to manage products, suppliers, categories, and customers.
It demonstrates the connection between frontend templates (HTML + Jinja), backend logic (Flask routes), and the database layer (SQLAlchemy ORM).

### ⚙️ Features
- Manage **suppliers**, **categories**, and **customers**
- Use **HTML forms** to send data to Flask
- Data is stored in a **SQLite database**

### ▶️ How to Run
```bash
# 1. Activate virtual environment (Windows example)
venv\Scripts\activate

# 2. Run the app
python app.py

# 3. Open in browser
http://127.0.0.1:5000

-----------------------------------------------------------------------------------------------------------------------

📘 Opis

To jest prosta aplikacja webowa napisana w Flask i SQLite, służąca do zarządzania produktami, dostawcami, kategoriami i klientami.
Pokazuje, jak frontend (HTML + Jinja2) komunikuje się z backendem (Flask) i bazą danych (SQLAlchemy ORM).

⚙️ Funkcje

Zarządzanie dostawcami, kategoriami i klientami

Formularze HTML przesyłają dane do Flask

Dane zapisywane są w bazie SQLite

▶️ Jak uruchomić
```bash
# 1.
venv\Scripts\activate

# 2. Run
python app.py

# 3. Następnie otwórz przeglądarkę i przejdź do:
http://127.0.0.1:5000

-----------------------------------------------------------------------------------------------------------------------

📘 Описание

Это простое веб-приложение на Flask и SQLite для управления товарами, поставщиками, категориями и клиентами.
Проект демонстрирует, как фронтенд (HTML + Jinja2) взаимодействует с Flask и базой данных через ORM (SQLAlchemy).

⚙️ Возможности

Управление поставщиками, категориями и клиентами

Ввод данных через HTML-формы

Хранение данных в SQLite

🧩 Как это работает

Пользователь открывает страницу (например /add_product)

Flask получает из базы список поставщиков и категорий

HTML-шаблон отображает форму

Пользователь вводит данные и отправляет

Flask принимает форму и сохраняет запись в базу

Пользователь перенаправляется на главную страницу с обновлённым списком

▶️ Как запустить

1. venv\Scripts\activate

2. python app.py

3. Затем открой:
http://127.0.0.1:5000


🧱 Technologies
Python 3
Flask
SQLAlchemy
SQLite
Jinja2