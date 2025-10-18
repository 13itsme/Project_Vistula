from flask import render_template, request, redirect, url_for #jinja шаблоны, объекты запроса
from app import app, db # Импорт flask объекта app и базы db
from models import Product, Supplier, Category, Customer


# Создание таблиц в БД если их еще нет при помощи SQLAlchemy
with app.app_context():
    db.create_all()

# PRODUCTS
# Главная страница
@app.route('/')
def index():
    products = Product.query.all() # Все строки из таблицы product
    return render_template('index.html', products=products)

# Добавление продуктов
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    suppliers = Supplier.query.all()
    categories = Category.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        supplier_id = request.form.get('supplier_id')
        category_id = request.form.get('category_id')

        new_product = Product(
            name=name,
            price=price,
            supplier_id=supplier_id or None,
            category_id=category_id or None
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index')) # Возвращает на главную

    return render_template('add_product.html', suppliers=suppliers, categories=categories)

# SUPPLIERS
@app.route('/suppliers')
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/add_supplier', methods=['GET', 'POST']) # GET страница обновления. POST страница обработки добавления
def add_supplier():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        new_supplier = Supplier(name=name, phone=phone)
        db.session.add(new_supplier)
        db.session.commit()
        return redirect(url_for('suppliers'))
    return render_template('add_supplier.html')

# CATEGORIES
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

# CUSTOMERS
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
