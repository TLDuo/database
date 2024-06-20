from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template

client_list_bp = Blueprint('client_list', __name__)
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

@client_list_bp.route('/client_list')
def research_client_list():
    #查询客户名单
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM customer"
    cursor.execute(query)
    clients = cursor.fetchall()
    cursor.close()
    return render_template('client_list.html', clients=clients)

def client_list_init_routes(app):
    app.register_blueprint(client_list_bp)