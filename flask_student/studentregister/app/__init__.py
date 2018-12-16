# _*_ coding: utf-8 _*_
__author__ = 'FWJ'
__date__ = 2017 / 12 / 24
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os


excel_dir = os.path.abspath('..')

# 设置数据库
# 官方文档：http://www.pythondoc.com/flask-sqlalchemy/config.html#id2
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@mysql:3306/studentmessage"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
"""
   官方文档：http://docs.jinkan.org/docs/flask-wtf/csrf.html
   然后在模板那里设置
   <form method="post" action="/">
    {{ form.csrf_token }}
   </form>
"""
app.config["SECRET_KEY"] = '576d589b1ab347d88a860592f9497cb3'
# 打开调试
app.debug = False
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
# 注册蓝图
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/teachermanage")


# 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
