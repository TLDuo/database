from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template

login_bp = Blueprint('login', __name__)
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

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            #session['username'] = user[0]  # 确保这里是正确的用户名字段
            #设置user表中log_in字段为1
            cursor = conn.cursor()
            query = "UPDATE user SET log_in = 1 WHERE username = %s"
            cursor.execute(query, (username,))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/profile/{}'.format(username))  # 重定向到个人主页
        else:
            flash('登录失败，请检查用户名和密码是否正确！')  # 使用 flash 发送消息
            return redirect('/login')
    else:
        return render_template('login.html')
    
@login_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    #session.pop('username', None)
    #设置user表中log_in字段为0
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("CALL log_update(@output_signal)")
    print(1)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/login')

def login_init_routes(app):
    app.register_blueprint(login_bp)