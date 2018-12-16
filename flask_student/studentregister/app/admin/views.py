# _*_ coding: utf-8 _*_
__author__ = 'FWJ'
__date__ = 2017 / 12 / 24
from . import admin
from app.models import StudentMessage, ClassName, Admin
import pandas as pd
from flask import render_template, flash, redirect, url_for, make_response, request, send_file, session
from app.admin.forms import ClassAddForm, SaveForm, LoginForm
from app import db, excel_dir
import os
from functools import wraps


def classname():
    test = []
    for i in ClassName.query.all():
        if ClassName.query.filter_by(name=i.name).first().class_excel == 1:
            test.append(i.name)
    return test


# class SaveExcel():
#     name = [('0', '请选择班级'), ]
#     for x in ClassName.query.all():
#         c = []
#         c.append(str(x.id))
#         c.append(x.name)
#         d = tuple(c)
#         name.append(d)


# 登录页面访问控制
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            # next是为了重新登录之后进入之前的网址
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# 登录
@admin.route("/login/", methods=["GET", "POST"])
def login():
    # 表单实例化
    form = LoginForm()
    # 提交的时候进行验证
    if form.validate_on_submit():
        # 获取表单信息
        data = form.data
        # query文档：http://www.cnblogs.com/agmcs/p/4445583.html
        # 官方文档：http://www.pythondoc.com/flask-sqlalchemy/queries.html?highlight=filter_by
        # http://blog.csdn.net/sun_dragon/article/details/51719753
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误！")
            return redirect(url_for("admin.login"))
        # 保存账号
        session["admin"] = data["account"]
        # http://docs.jinkan.org/docs/flask/api.html?highlight=request#flask.request
        # flask中request的args用法，以我现在的理解是获取请求参数里面的网页
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 退出登录
@admin.route("/logout/")
@admin_login_req
def logout():
    # 点击退出删除账号
    session.pop("admin", None)
    return redirect(url_for("admin.login"))


# 主页
@admin.route("/")
@admin_login_req
def index():

    return render_template('admin/admin.html')


# 添加班级
@admin.route("/class/add", methods=['POST', 'GET'])
@admin_login_req
def class_add():
    form = ClassAddForm()
    if form.validate_on_submit():
        data = form.data
        class_name = ClassName.query.filter_by(name=data["class_add"]).count()
        if class_name == 1:
            flash("名称已经存在！", "err")
            return redirect(url_for('admin.class_add'))
        class_name = ClassName(
            name=data["class_add"]
        )
        db.session.add(class_name)
        db.session.commit()
        flash("添加班级成功", "ok")
        redirect(url_for("admin.class_add"))

    return render_template("admin/class_add.html", form=form)


# 保存学生信息
@admin.route("/class/list", methods=["GET", "POST"])
@admin_login_req
def class_list():
    # 保存表格
    form = SaveForm()
    # 班级显示
    classname1 = classname()
    if form.validate_on_submit():
        data = form.data
        classname_id = ClassName.query.filter_by(name=data['class_name']).first().id
        class_id = []
        name = []
        sex = []
        age = []
        card = []
        phone = []
        qq = []
        email = []
        education = []
        school = []
        specialty = []
        family = []
        familyphone = []
        familyadd = []
        guangzhouadd = []
        apply = []
        id = []
        data = StudentMessage
        data_all = data.query.filter_by(class_id=classname_id).all()
        # classnameid = ClassName.query.filter_by(id=classname_id).all()
        i = len(data_all)
        for e in range(i):
            id.append(data_all[e].id)
            name.append(data_all[e].name)  # 姓名
            sex.append(data_all[e].sex)  # 性别
            age.append(data_all[e].age)  # 年龄
            card.append(data_all[e].card)  # 身份证
            phone.append(data_all[e].phone)  # 手机号码
            qq.append(data_all[e].qq)  # qq号
            email.append(data_all[e].email)  # 邮箱
            education.append(data_all[e].education)  # 学历
            school.append(data_all[e].school)  # 毕业学校
            specialty.append(data_all[e].specialty)  # 专业
            family.append(data_all[e].family)  # 家庭联系人
            familyphone.append(data_all[e].familyphone)  # 家庭联系人电话
            guangzhouadd.append(data_all[e].guangzhouadd)  # 广州地址
            familyadd.append(data_all[e].familyadd)  # 家庭地址
            apply.append(data_all[e].apply)  # 报名渠道
            class_id.append(data_all[e].class_id)   # 班级id

        df = pd.DataFrame({'id': id,
                           '姓名': name,
                           '性别': sex,
                           '年龄': age,
                           '身份证号码': card,
                           '手机号码': phone,
                           'qq号码': qq,
                           '邮箱地址': email,
                           '学历': education,
                           '毕业学校': school,
                           '专业': specialty,
                           '家庭联系人': family,
                           '家庭联系人号码': familyphone,
                           '广州住址': guangzhouadd,
                           '家庭地址': familyadd,
                           '报名渠道': apply,
                           '班级id': class_id
                           })

        # 导入excel表
        classexcel = ClassName.query.filter_by(id=classname_id).first().class_excel
        if classexcel == 1:
            flash("excel表已存在，请删除后再重试", "err")
            return redirect(url_for('admin.class_list'))
        else:
            # 保存数据
            # 修改class_excel值
            ClassName.query.filter(ClassName.id == classname_id).update({'class_excel': 1})
            db.session.commit()
            class_name = ClassName.query.filter_by(id=classname_id).first().name
            excel_file = class_name + '.xlsx'
            df.to_excel(excel_file, sheet_name='sheet1')
            flash("信息导入成功", "ok")
            return redirect(url_for('admin.class_list'))
    return render_template("admin/class_list.html", class_name=classname1, form=form)


# 下载
@admin.route("/download", methods=['GET', 'POST'])
def file_download():
    fileName = request.args.get("fileName")
    file = os.path.abspath(".") + '\\' + fileName + '.xlsx'
    response = make_response(send_file(file))
    # 解决中文问题
    response.headers["Content-Disposition"] = "attachment; filename={};".format(file.encode().decode('latin-1'))
    return response


# 删除excel文档
@admin.route("/delete", methods=['GET'])
def file_delete():
    fileName = request.args.get('fileName')
    file = os.path.abspath('.') + '\\' + fileName + '.xlsx'
    os.remove(file)
    # 修改class_excel值
    classname_id = ClassName.query.filter_by(name=fileName).first().id
    ClassName.query.filter(ClassName.id == classname_id).update({'class_excel': 0})
    db.session.commit()
    return redirect(url_for('admin.class_list'))