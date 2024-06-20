from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template
#获取日期
from datetime import datetime

save_account_bp = Blueprint('save_account', __name__)
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

@save_account_bp.route('/save_account_list', methods=['GET', 'POST'])
def search_save_account_list():
    #查询储蓄账户名单
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM save_account"
    cursor.execute(query)
    accounts = cursor.fetchall()
    cursor.close()
    return render_template('save_account_list.html', accounts=accounts)

@save_account_bp.route('/save_account_list/add_save_account', methods=['GET', 'POST'])
def add_save_account():
    #添加储蓄账户
    if request.method == 'POST':
        #account_id = request.form.get('account_id')
        person_id = request.form.get('person_id')
        bank_name = request.form.get('bank_name')
        password = request.form.get('password')
        remaining = request.form.get('remaining')
        worker_id = request.form.get('worker_id')
        #获取现在日期
        open_date = datetime.now().strftime('%Y-%m-%d')
        rate = request.form.get('rate')
        if not person_id or not bank_name or not password or not remaining or not open_date or not rate:
            return '必须提供账户ID、个人ID、银行名称、密码、余额、开户日期和利率！'
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("CALL max_account_id(@output_signal)")
        cursor.execute("SELECT @output_signal")
        account_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO account (account_id, client_person_id, bank_name, password, remaining, open_date) VALUES (%s, %s, %s, %s, %s, %s)", (account_id, person_id, bank_name, password, remaining, open_date))
        conn.commit()
        query = "INSERT INTO save_account (account_id, person_id, bank_name, password, remaining, open_date, rate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (account_id, person_id, bank_name, password, remaining, open_date, rate))
        conn.commit()
        cursor.execute("INSERT INTO serve_list (worker_id, client_person_id, serve_date, serve_type) VALUES (%s, %s, %s, %s)", (worker_id, person_id, datetime.now(), '开设储蓄账户'))
        conn.commit()
        cursor.close()
        return redirect('/save_account_list')
    else:
        return render_template('add_save_account.html')

    

def save_account_init_routes(app):
    app.register_blueprint(save_account_bp)