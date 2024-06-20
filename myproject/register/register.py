from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template

register_bp = Blueprint('register', __name__)
import pymysql
import secrets

def connect_to_db():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        database='bank_db',
        charset='utf8'
    )
    return conn

def check_username_exists(username):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    return user is not None

def insert_new_user(username, password):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO user (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    conn.commit()
    cursor.close()

register_bp.secret_key = secrets.token_hex(16)
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form.get('password_confirm')
        if password != password_confirm:
            return '两次输入的密码不一致，请重新输入！'
        if check_username_exists(username):
            return '用户名已经存在，请选择一个不同的用户名！'
        insert_new_user(username, password)
        #为新用户往images表中插入一条初始记录
        conn = connect_to_db()
        cursor = conn.cursor()
        filename = '../static/images/1707496853306.jpg'
        query = "INSERT INTO images (username, image_path) VALUES (%s, %s)"
        params = (username, filename)
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/register_success')
    else:
        return render_template('register.html')

@register_bp.route('/register_success')
def register_success():
    return render_template('register_success.html')

def register_init_routes(app):
    app.register_blueprint(register_bp)