import sqlite3
from datetime import datetime

DATABASE = 'dostavka.db'

def execute_query(query, params=(), commit=False):
    """Выполняет запрос к базе данных и возвращает результат, если требуется."""
    with sqlite3.connect(DATABASE, timeout=10) as db:
        cursor = db.cursor()
        cursor.execute(query, params)
        if commit:
            db.commit()
        return cursor

def create_tables():
    queries = [
        '''CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER PRIMARY KEY,
            name TEXT,
            phone_number TEXT,
            address TEXT,
            reg_date DATETIME
        );''',
        '''CREATE TABLE IF NOT EXISTS products (
            pr_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pr_name TEXT,
            pr_price REAL,
            pr_quantity INTEGER,
            pr_des TEXT,
            pr_photo TEXT,
            reg_date DATETIME
        );''',
        '''CREATE TABLE IF NOT EXISTS user_cart (
            user_id INTEGER,
            user_product INTEGER,
            quantity INTEGER,
            total_for_price REAL,
            FOREIGN KEY (user_product) REFERENCES products(pr_id)
        );'''
    ]
    for query in queries:
        execute_query(query, commit=True)

def register_user(tg_id, name, phone_number, address):
    query = '''INSERT INTO users (tg_id, name, phone_number, address, reg_date)
               VALUES (?, ?, ?, ?, ?);'''
    execute_query(query, (tg_id, name, phone_number, address, datetime.now()), commit=True)

def check_user(user_id):
    query = 'SELECT tg_id FROM users WHERE tg_id=?;'
    result = execute_query(query, (user_id,))
    return result.fetchone() is not None

def add_product(pr_name, pr_price, pr_quantity, pr_des, pr_photo):
    query = '''INSERT INTO products (pr_name, pr_price, pr_quantity, pr_des, pr_photo, reg_date)
               VALUES (?, ?, ?, ?, ?, ?);'''
    execute_query(query, (pr_name, pr_price, pr_quantity, pr_des, pr_photo, datetime.now()), commit=True)


def delete_all_products():
    # Удаление всех записей из таблицы user_cart, связанных с продуктами
    query_cart = 'DELETE FROM user_cart;'
    execute_query(query_cart, commit=True)

    # Удаление всех продуктов из таблицы products
    query_products = 'DELETE FROM products;'
    execute_query(query_products, commit=True)

    print("Все продукты успешно удалены из базы данных.")

def delete_product(product_id):
    # Удаление всех записей из таблицы user_cart, связанных с этим продуктом
    query_cart = 'DELETE FROM user_cart WHERE user_product=?;'
    execute_query(query_cart, (product_id,), commit=True)

    # Удаление продукта из таблицы products
    query_product = 'DELETE FROM products WHERE pr_id=?;'
    execute_query(query_product, (product_id,), commit=True)

    print(f"Продукт с ID {product_id} успешно удален из базы данных.")

def delete_all_users():
    # Удаление всех записей из таблицы user_cart, связанных с продуктами
    query_cart = 'DELETE FROM users;'
    execute_query(query_cart, commit=True)

    print("Все пользователи успешно удалены из базы данных.")

def delete_user(user_id):
    # Удаление всех записей из таблицы user_cart, связанных с этим пользователем
    query_cart = 'DELETE FROM user_cart WHERE user_id=?;'
    execute_query(query_cart, (user_id,), commit=True)

    # Удаление пользователя из таблицы users
    query_user = 'DELETE FROM users WHERE tg_id=?;'
    execute_query(query_user, (user_id,), commit=True)

    print(f"Пользователь с ID {user_id} успешно удален из базы данных.")

def get_pr_name_id():
    query = 'SELECT pr_id, pr_name, pr_quantity FROM products;'
    products = execute_query(query).fetchall()
    return [(name, pr_id) for pr_id, name, quantity in products if quantity > 0]

def get_pr_id():
    query = 'SELECT pr_id, pr_quantity FROM products;'
    products = execute_query(query).fetchall()
    return [pr_id for pr_id, quantity in products if quantity > 0]

def get_product_id(pr_id):
    query = 'SELECT pr_price FROM products WHERE pr_id=?;'
    result = execute_query(query, (pr_id,))
    row = result.fetchone()
    return row[0] if row else None

def add_product_to_cart(user_id, user_product, quantity):
    product_price = get_product_id(user_product)
    if product_price is None:
        raise ValueError("Product not found.")
    total_price = quantity * product_price
    query = '''INSERT INTO user_cart (user_id, user_product, quantity, total_for_price)
               VALUES (?, ?, ?, ?);'''
    execute_query(query, (user_id, user_product, quantity, total_price), commit=True)

def delete_product_from_cart(user_id):
    query = 'DELETE FROM user_cart WHERE user_id=?;'
    execute_query(query, (user_id,), commit=True)

def get_exact_user_cart(user_id):
    query = '''SELECT products.pr_name, user_cart.quantity, user_cart.total_for_price
               FROM products
               INNER JOIN user_cart ON products.pr_id = user_cart.user_product
               WHERE user_cart.user_id=?;'''
    return execute_query(query, (user_id,)).fetchall()

def get_user_number_name(user_id):
    query = 'SELECT name, phone_number FROM users WHERE tg_id=?;'
    return execute_query(query, (user_id,)).fetchone()


def get_product_details(pr_id):
    query = '''SELECT pr_name, pr_des, pr_photo FROM products WHERE pr_id=?;'''
    result = execute_query(query, (pr_id,)).fetchone()

    if result:
        pr_name, pr_des, pr_photo = result
        return {
            'name': pr_name,
            'description': pr_des,
            'photo': pr_photo
        }
    else:
        return None