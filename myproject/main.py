from flask import Flask, render_template, request, redirect, url_for, flash, session
#连接数据库
import pymysql
import secrets

from register.register import register_init_routes
from login.login import login_init_routes
from worker_list.worker_list import worker_list_init_routes
from profile.profile import profile_init_routes
from client_list.client_list import client_list_init_routes
from account_list.save_account_list import save_account_init_routes
from account_list.credit_account_list import credit_account_init_routes
from bank.bank import bank_init_routes
from department.department import department_init_routes
from loan.loan import loan_init_routes
from serve_list.serve_list import history_init_routes

# 创建连接

# 2.创建连接对象



def connect_to_db():
    conn = pymysql.connect(
    host='localhost',    # 本机就写：localhost
    port=3306,                 # 要连接到的数据库端口号，MySQL是3306
    user='root',                # 数据库的用户名
    password='123456',            # 数据库的密码
    database='bank_db',      # 要操作的数据库
    charset='utf8'             # 码表
    )
    return conn

#搭建蓝图
app = Flask(__name__)
register_init_routes(app)
login_init_routes(app)
worker_list_init_routes(app)
profile_init_routes(app)
client_list_init_routes(app)
save_account_init_routes(app)
credit_account_init_routes(app)
bank_init_routes(app)
department_init_routes(app)
loan_init_routes(app)
history_init_routes(app)
# 生成随机密钥
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return redirect('/login')
    

# 关闭游标
#cursor.close()#

# 关闭连接
#conn.close()
if __name__ == "__main__":
    app.run(debug=True)