# _*_ coding: utf-8 _*_
__author__ = 'FWJ'
__date__ = 2017 / 12 / 24
from . import home
from flask import render_template, redirect, url_for, flash
from app import db
from app.models import StudentMessage, ClassName
from app.home.forms import StudentForm
import os
import xlwt


@home.route('/', methods=['POST', 'GET'])
def studentmessage():
    form = StudentForm()
    if form.validate_on_submit():
        data =form.data
        name = StudentMessage.query.filter_by(name=data["name"]).count()
        if name == 1:
            flash("名字已经存在", "err")
            return redirect(url_for('home.studentmessage'))
        name = StudentMessage(
            name=data["name"],
            sex=data["sex"],
            age=data["age"],
            card=data["card"],
            phone=data["phone"],
            qq=data["qq"],
            email=data["email"],
            education=data["education"],
            school=data["school"],
            specialty=data["specialty"],
            family=data["family"],
            familyphone=data["familyphone"],
            guangzhouadd=data["guangzhouadd"],
            familyadd=data["familyadd"],
            apply=data["apply"],
            class_id=ClassName.query.filter_by(name=data['class_name']).first().id
        )
        # 保存数据
        db.session.add(name)
        db.session.commit()
        flash("信息添加成功", "ok")
        redirect(url_for('home.studentmessage'))
    return render_template('home/index.html', form=form)