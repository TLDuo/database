from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template
from datetime import datetime

history_bp = Blueprint('history', __name__)
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

@history_bp.route('/history', methods=['GET', 'POST'])
def research_history_list():
    #查询贷款名单
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM serve_list"
    cursor.execute(query)
    historys = cursor.fetchall()
    cursor.close()
    return render_template('serve_list.html', historys=historys)

@history_bp.route('/serve_search', methods=['GET', 'POST'])
def research_serve_history_list():
    #查询贷款名单
    worker_id = request.form.get('worker_id')
    conn = connect_to_db()
    cursor = conn.cursor()
    #get_service_count(worker_id_param CHAR(16))
    query = "SELECT get_service_count(%s)"
    cursor.execute(query, (worker_id,))
    # 获取返回结果
    service_count = cursor.fetchone()[0]  # 假设函数返回单个值
    #获取对应工作人员的服务记录
    query = "SELECT * FROM serve_list WHERE worker_id = %s"
    cursor.execute(query, (worker_id,))
    historys = cursor.fetchall()
    cursor.close()
    return render_template('serve_research_list.html', worker_id = worker_id,service_count=service_count, historys=historys)

def history_init_routes(app):
    app.register_blueprint(history_bp)
