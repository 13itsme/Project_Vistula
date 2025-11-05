from flask import render_template, request, redirect, url_for, jsonify, session
from app import app, db
from models import Product, Supplier, Category, Customer, User
from werkzeug.security import generate_password_hash, check_password_hash


# === Контекстный процессор ===
@app.context_processor
def inject_user_status():
    return {'logged_in': 'user_id' in session}


# === Главная страница (Products) ===
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


# === Поставщики ===
@app.route('/suppliers')
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)


# === Категории ===
@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


# === Клиенты ===
@app.route('/customers')
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)


# === Добавление продукта ===
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        new_product = Product(name=name, price=price)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')


# === Добавление поставщика ===
@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        new_supplier = Supplier(name=name, phone=phone)
        db.session.add(new_supplier)
        db.session.commit()
        return redirect(url_for('suppliers'))
    return render_template('add_supplier.html')


# === Добавление категории ===
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('add_category.html')


# === Добавление клиента ===
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_customer = Customer(name=name, email=email)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('customers'))
    return render_template('add_customer.html')


# === Универсальное редактирование ===
@app.route('/edit/<model>/<int:item_id>', methods=['GET', 'POST'])
def edit_item(model, item_id):
    model_map = {
        'product': Product,
        'supplier': Supplier,
        'category': Category,
        'customer': Customer
    }

    Model = model_map.get(model)
    if not Model:
        return "Invalid model", 404

    item = Model.query.get_or_404(item_id)

    if request.method == 'POST':
        for key, value in request.form.items():
            if hasattr(item, key):
                setattr(item, key, value)
        db.session.commit()
        if model == 'product':
            return redirect(url_for('index'))
        else:
            return redirect(url_for(f"{model}s"))

    # === Исправление return_page ===
    return_page = 'index' if model == 'product' else f"{model}s"
    return render_template('edit_item.html', item=item, model=model, return_page=return_page)


# === Удаление ===
@app.route('/delete/<model>/<int:item_id>', methods=['POST'])
def delete_item(model, item_id):
    model_map = {
        'product': Product,
        'supplier': Supplier,
        'category': Category,
        'customer': Customer
    }

    Model = model_map.get(model)
    if not Model:
        return "Invalid model", 404

    item = Model.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    if model == 'product':
        return redirect(url_for('index'))
    else:
        return redirect(url_for(f"{model}s"))


# === Регистрация ===
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form.get('email', '')  # если ты хочешь хранить email

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    user = User(username=username, email=email)
    user.set_password(password)  # <— тут теперь используется метод из модели
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 200


# === Логин ===
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):  # <— заменено на метод модели
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


# === Логаут ===
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
