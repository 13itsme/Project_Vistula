from flask import render_template, request, redirect, url_for, jsonify, session
from app import app, db
from models import Product, Supplier, Category, Customer, User


# === Создание БД ===
with app.app_context():
    db.create_all()


# === Главная страница (Products) ===
@app.route('/')
def index():
    products = Product.query.all()
    logged_in = 'user_id' in session
    return render_template('index.html', products=products, logged_in=logged_in)


# === Добавление продукта ===
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    suppliers = Supplier.query.all()
    categories = Category.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        supplier_id = request.form.get('supplier_id')
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        stock = request.form.get('stock', 0)

        new_product = Product(
            name=name,
            price=price,
            supplier_id=supplier_id or None,
            category_id=category_id or None,
            description=description,
            stock=stock
        )

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_product.html', suppliers=suppliers, categories=categories)


# === Поставщики ===
@app.route('/suppliers')
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)


@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')

        new_supplier = Supplier(name=name, phone=phone)
        db.session.add(new_supplier)
        db.session.commit()
        return redirect(url_for('suppliers'))

    return render_template('add_supplier.html')


# === Категории ===
@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('add_category.html')


# === Клиенты ===
@app.route('/customers')
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        new_customer = Customer(name=name, email=email)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('customers'))

    return render_template('add_customer.html')


# === Регистрация ===
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 409

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id
    return jsonify({"message": "User registered successfully"}), 201


# === Logout ===
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"}), 200


# login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    session['user_id'] = user.id
    return jsonify({"message": "Login successful"}), 200


# === УДАЛЕНИЕ ===
@app.route('/delete/<string:model>/<int:item_id>', methods=['POST'])
def delete_item(model, item_id):
    models = {
        'product': Product,
        'supplier': Supplier,
        'category': Category,
        'customer': Customer
    }
    model_class = models.get(model)
    if not model_class:
        return jsonify({"error": "Invalid model"}), 400

    item = model_class.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))


# === Редактирование ===
@app.route('/edit/<string:model>/<int:item_id>', methods=['GET', 'POST'])
def edit_item(model, item_id):
    models = {
        'product': Product,
        'supplier': Supplier,
        'category': Category,
        'customer': Customer
    }
    model_class = models.get(model)
    if not model_class:
        return jsonify({"error": "Invalid model"}), 400

    item = model_class.query.get_or_404(item_id)

    if request.method == 'POST':
        if model == 'product':
            item.name = request.form['name']
            item.price = request.form['price']
            item.description = request.form.get('description')
            item.stock = request.form.get('stock', 0)
            return_page = 'index'

        elif model == 'supplier':
            item.name = request.form['name']
            item.phone = request.form.get('phone')
            return_page = 'suppliers'

        elif model == 'category':
            item.name = request.form['name']
            return_page = 'categories'

        elif model == 'customer':
            item.name = request.form['name']
            item.email = request.form.get('email')
            return_page = 'customers'

        db.session.commit()
        return redirect(url_for(return_page))

    # Определяем страницу возврата
    return_page = {
        'product': 'index',
        'supplier': 'suppliers',
        'category': 'categories',
        'customer': 'customers'
    }.get(model, 'index')

    return render_template('edit_item.html', model=model, item=item, return_page=return_page)
