from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template

worker_list_bp = Blueprint('worker', __name__)
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

@worker_list_bp.route('/worker_list')
def research_worker_list():
    #查询员工名单
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM worker"
    cursor.execute(query)
    workers = cursor.fetchall()
    cursor.close()
    return render_template('worker_list.html', workers=workers)

@worker_list_bp.route('/add_worker', methods=['GET', 'POST'])
def add_worker():
    if request.method == 'POST':
        worker_id = request.form.get('worker_id')
        department_id = request.form.get('department_id')
        worker_name = request.form.get('worker_name')
        worker_sex = request.form.get('worker_sex')
        worker_person_id = request.form.get('worker_person_id')
        worker_level = request.form.get('worker_level')
        worker_number = request.form.get('worker_number')
        worker_address = request.form.get('worker_address')
        # 插入员工信息
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "INSERT INTO worker (worker_id, department_id, worker_name, worker_sex, worker_person_id, worker_level, worker_number, worker_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (worker_id, department_id, worker_name, worker_sex, worker_person_id, worker_level, worker_number, worker_address))
        conn.commit()
        cursor.close()
        return redirect('/worker_list')
    else:
        return render_template('add_worker.html')
    
@worker_list_bp.route('/delete_worker', methods=['GET', 'POST'])
def delete_worker():
    if request.method == 'POST':
        worker_id = request.form.get('worker_id')
        department_id = request.form.get('department_id')
        worker_name = request.form.get('worker_name')  # 修正了变量名的拼写错误
        if not worker_id or not department_id or not worker_name:
            return '必须提供员工ID、部门ID和员工姓名！'
        conn = connect_to_db()
        cursor = conn.cursor()
        # 检查是否存在
        cursor.execute("SELECT * FROM worker WHERE worker_id = %s AND department_id = %s AND worker_name = %s", (worker_id, department_id, worker_name))
        worker = cursor.fetchone()
        if not worker:
            cursor.close()
            return '员工不存在！'
        
        cursor.execute("CALL delete_worker(%s, %s, %s, @output_signal)", (worker_id, department_id, worker_name))
        conn.commit()
        cursor.execute("SELECT @output_signal")
        output_signal = cursor.fetchone()[0]
        cursor.close()
        return redirect('/worker_list')
    else:
        return render_template('delete_worker.html')

def worker_list_init_routes(app):
    app.register_blueprint(worker_list_bp)