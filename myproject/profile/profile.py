from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template

profile_bp = Blueprint('profile', __name__)
import pymysql
import secrets
import os

from pymysql import Error

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

def save_to_db(username,filename):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        #查询数据库中是否有该用户的图片路径
        cursor.execute("SELECT * FROM images WHERE username = %s", (username,))
        user = cursor.fetchone()
        #如果没有就插入
        if not user:
            query = "INSERT INTO images (username, image_path) VALUES (%s, %s)"
            params = (username, filename)
            cursor.execute(query, params)
            conn.commit()
            cursor.close()
            conn.close()
            return
        # 更新数据库中的文件路径
        query = "UPDATE images SET image_path = %s WHERE username = %s"
        params = (filename, username)
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(e)

def get_user_image(username):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            #print(username)
            cursor.execute("SELECT image_path FROM images WHERE username = %s", (username,))
            image_path = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return image_path
        except Error as e:
            print(e)

@profile_bp.route('/profile', methods=['GET', 'POST'])
def login_success():
    #查询user表中log_in字段为1的用户
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT username FROM user WHERE log_in = 1"
    cursor.execute(query)
    username = cursor.fetchone()[0]
    if(username == None):
        cursor.close()
        conn.close()
        return redirect('/login')
    cursor.close()
    conn.close()
    #获取用户图片路径
    image_path = get_user_image(username)

    return render_template('profile.html', username=username, image_path=image_path)
    
@profile_bp.route('/profile/<username>')
def profile(username):
    # 假设有一个函数 get_user_image(username) 获取用户图片路径
    #从数据库中获取对应用户的图片路径
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT username FROM user WHERE log_in = 1"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        cursor.close()
        conn.close()
        return redirect('/login')
    image_path = get_user_image(username)
    print(image_path)
    return render_template('profile.html', username=username, image_path=image_path)
    
@profile_bp.route('/upload/<username>', methods=['GET', 'POST'])
def upload(username):
    if request.method == 'POST':
        file = request.files['image']  # 从请求中获取文件
        filename = os.path.join(os.getcwd(),'static\\images', file.filename)  # 拼接文件绝对路径
        file.save(filename)   # 将文件保存到本地文件系统
        #获取图片相对位置
        filename = '../static/images/' + file.filename
        save_to_db(username, filename)  # 将文件路径存储到数据库中
        return redirect(url_for('profile.profile', username=username))

    

    
def profile_init_routes(app):
    app.register_blueprint(profile_bp)