from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template

department_bp = Blueprint('department', __name__)
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

@department_bp.route('/department', methods=['GET', 'POST'])
def research_department_list():
    #查询银行名单
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM department"
    cursor.execute(query)
    departments = cursor.fetchall()
    cursor.close()
    return render_template('department.html', departments=departments)

@department_bp.route('/add_department', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        department_id = request.form.get('department_id')
        bank_name = request.form.get('bank_name')
        department_name = request.form.get('department_name')
        department_type = request.form.get('department_type')
        # 插入银行信息
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "INSERT INTO department (department_id, bank_name, department_name, department_type) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (department_id, bank_name, department_name, department_type))
        conn.commit()
        cursor.close()
        return redirect('/department')
    else:
        return render_template('add_department.html')
    
@department_bp.route('/update_department', methods=['POST'])
def update_bank():
    key = request.form.get('key')
    old_department_id = request.form.get('old_department_id')
    new_department_id = request.form.get('new_department_id')
    bank_name = request.form.get('bank_name')
    department_name = request.form.get('department_name')
    department_type = request.form.get('department_type')
    # 老银行名不存在，不能改
    conn = connect_to_db()
    cursor = conn.cursor()
    if not new_department_id or not old_department_id:  # 检查部门号是否为空
        return '部门ID不能为空！'
    cursor.execute("SELECT * FROM department WHERE department_id = %s", (old_department_id,))
    department_exists = cursor.fetchone()
    if not department_exists:
        return '部门不存在！'
    # 更新部门信息
    cursor.execute("SELECT * FROM department WHERE department_id = %s and bank_name = %s", (old_department_id,bank_name,))
    department_exists = cursor.fetchone()
    if not department_exists:
        return '部门与银行不匹配！'
    if not bank_name:  # 检查银行是否为空
        return '银行名称不能为空！'
    cursor.execute("SELECT * FROM bank WHERE bank_name = %s", (bank_name,))
    bank_exists = cursor.fetchone()
    if not bank_exists:
        return '银行不存在！'
    # 更新银行信息  
    #print(old_bank_name, new_bank_name)
    if int(key) == 1:
        if old_department_id == new_department_id:
            return '新部门ID不能与旧部门ID相同！'
        cursor.execute("CALL renum_department(%s, %s, @output_signal)", (old_department_id, new_department_id))
        conn.commit()
        #print(new_bank_name, old_bank_name)
        cursor.execute("SELECT @output_signal")
        output_signal = cursor.fetchone()[0]
        #print(1)
        # 根据输出信号处理逻辑
        if output_signal != 1:
            return '部门ID已存在！'
        cursor.execute("UPDATE department SET  department_name = %s, department_type = %s WHERE department_id = %s", (department_name, department_type, new_department_id))
        conn.commit()
        cursor.close()
        return redirect('/department')
    else:
        cursor.execute("UPDATE department SET  department_name = %s, department_type = %s WHERE department_id = %s", (department_name, department_type, old_department_id))
        conn.commit()
        cursor.close()
        return redirect('/department')

def department_init_routes(app):
    app.register_blueprint(department_bp)