from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template

bank_bp = Blueprint('bank', __name__)
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

@bank_bp.route('/bank', methods=['GET', 'POST'])
def research_bank_list():
    #查询银行名单
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM bank"
    cursor.execute(query)
    banks = cursor.fetchall()
    cursor.close()
    return render_template('bank.html', banks=banks)

@bank_bp.route('/add_bank', methods=['GET', 'POST'])
def add_bank():
    if request.method == 'POST':
        bank_name = request.form.get('bank_name')
        city = request.form.get('city')
        sum_remaining = request.form.get('sum_remaining')
        # 插入银行信息
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "INSERT INTO bank (bank_name, city, sum_remaining) VALUES (%s, %s, %s)"
        cursor.execute(query, (bank_name, city, sum_remaining))
        conn.commit()
        cursor.close()
        return redirect('/bank')
    else:
        return render_template('add_bank.html')
    
@bank_bp.route('/update_bank', methods=['POST'])
def update_bank():
    key = request.form.get('key')
    old_bank_name = request.form.get('old_bank_name')
    new_bank_name = request.form.get('new_bank_name')
    city = request.form.get('city')
    sum_remaining = request.form.get('sum_remaining')
    # 老银行名不存在，不能改
    conn = connect_to_db()
    cursor = conn.cursor()
    if not new_bank_name or not old_bank_name:  # 检查银行是否为空
        return '银行名称不能为空！'
    cursor.execute("SELECT * FROM bank WHERE bank_name = %s", (old_bank_name,))
    bank_exists = cursor.fetchone()
    if not bank_exists:
        return '银行不存在！'
    # 更新银行信息  
    #print(old_bank_name, new_bank_name)
    if int(key) == 1:
        if old_bank_name == new_bank_name:
            return '新银行名不能与旧银行名相同！'
        cursor.execute("CALL bank_rename(%s, %s, @output_signal)", (old_bank_name, new_bank_name))
        conn.commit()
        #print(new_bank_name, old_bank_name)
        cursor.execute("SELECT @output_signal")
        output_signal = cursor.fetchone()[0]
        #print(1)
        # 根据输出信号处理逻辑
        if output_signal != 1:  # 假设1表示成功
            return '银行信息更新失败！'
        cursor.execute("UPDATE bank SET city = %s, sum_remaining = %s WHERE bank_name = %s", (city, sum_remaining, new_bank_name))
        conn.commit()
        cursor.close()
        return redirect('/bank')
    else:
        cursor.execute("UPDATE bank SET city = %s, sum_remaining = %s WHERE bank_name = %s", (city, sum_remaining, old_bank_name))
        conn.commit()
        cursor.close()
        return redirect('/bank')

def bank_init_routes(app):
    app.register_blueprint(bank_bp)