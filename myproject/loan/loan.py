from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Blueprint, render_template
from datetime import datetime

loan_bp = Blueprint('loan', __name__)
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

@loan_bp.route('/loan', methods=['GET', 'POST'])
def research_loan_list():
    #查询贷款名单
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM loan where loan.loan_remain > 0"
    cursor.execute(query)
    loans = cursor.fetchall()
    cursor.close()
    return render_template('loan.html', loans=loans)

@loan_bp.route('/loan/pay_list', methods=['GET', 'POST'])
def research_pay_list():
    #查询还贷记录
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM pay_list"
    cursor.execute(query)
    pay_lists = cursor.fetchall()
    cursor.close()
    return render_template('pay_lists.html', pay_lists=pay_lists)

@loan_bp.route('/borrow_loan', methods=['POST'])
def borrow_loan():
    #定义status
    status = 1
    bank_name = request.form.get('bank_name')
    client_person_id = request.form.get('client_person_id')
    worker_id = request.form.get('worker_id');
    loan_total = request.form.get('loan_total')
    loan_rate = request.form.get('loan_rate')
    print(bank_name, client_person_id, loan_total, loan_rate)
    #连接数据库
    conn = connect_to_db()
    cursor = conn.cursor()
    # 调用sql过程procedure borrow_loan (IN client_id CHAR(18), IN bank_name CHAR(30), IN loan_total INT, IN loan_rate FLOAT,  OUT status INT)
    #cursor.execute("CALL renum_department(%s, %s, @output_signal)", (old_department_id, new_department_id))
    # 定义存储过程的参数，包括输入和输出参数
    proc_args = [client_person_id, bank_name, loan_total, loan_rate, 0]  # 假设最后一个参数是输出参数，初始值设为0
    cursor.callproc('borrow_loan', proc_args)
    # 提交事务
    conn.commit()
    #往serve_list中插入对应员工和客户的服务信息
    # 获取存储过程的输出参数
    cursor.execute("SELECT @_borrow_loan_4")  # 注意：这里的 @_borrow_loan_4 是根据存储过程的名称和输出参数的位置自动生成的变量名
    status = cursor.fetchone()[0]
    if(status != 1):
        return '借贷失败！'
    cursor.execute("INSERT INTO serve_list (worker_id, client_person_id, serve_date, serve_type) VALUES (%s, %s, %s, %s)", (worker_id, client_person_id, datetime.now(), '借贷'))
    conn.commit()
    cursor.close()
    return redirect('/loan')

@loan_bp.route('/return_loan', methods=['POST'])
def return_loan():
    #定义status
    status = -1
    worker_id = request.form.get('worker_id')
    loan_id = request.form.get('loan_id')
    pay_money = request.form.get('pay_money')
    #连接数据库
    conn = connect_to_db()
    cursor = conn.cursor()
    # 定义存储过程的参数，包括输入和输出参数
    proc_args = [loan_id, pay_money, 0]  # 假设最后一个参数是输出参数，初始值设为0
    cursor.callproc('return_loan', proc_args)
    # 提交事务
    conn.commit()
    cursor.execute("SELECT @_return_loan_2")  # 注意：这里的 @_borrow_loan_4 是根据存储过程的名称和输出参数的位置自动生成的变量名
    status = cursor.fetchone()[0]
    print(status)
    if(status != -1):
        return '还贷失败！'
    #通过loan_id查询client_person_id
    cursor.execute("SELECT client_person_id FROM loan WHERE loan_id = %s", (loan_id,))
    client_person_id = cursor.fetchone()[0]
    #往serve_list中插入对应员工和客户的服务信息
    cursor.execute("INSERT INTO serve_list (worker_id, client_person_id, serve_date, serve_type) VALUES (%s, %s, %s, %s)", (worker_id, client_person_id, datetime.now(), '还贷'))
    conn.commit()
    cursor.close()
    return redirect('/loan/pay_list')


def loan_init_routes(app):
    app.register_blueprint(loan_bp)