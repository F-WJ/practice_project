# _*_ coding: utf-8 _*_
__author__ = 'FWJ'
__date__ = 2017 / 12 / 24

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from app.models import ClassName
# http://blog.csdn.net/sun_dragon/article/details/51701542

# 查找班级
def query_factory():
    return [r.name for r in ClassName.query.all()]


# 班级id
def get_pk(obj):
    return ClassName.query.filter_by(name=obj).first().id


class StudentForm(FlaskForm):
    # classname = [('0', '请选择班级'), ]
    # for x in ClassName.query.all():
    #
    #     a = (x.id)  # id
    #     b = (x.name)  # 班级
    #     c = []
    #     c.append(str(a))
    #     c.append(b)
    #     d = tuple(c)
    #     classname.append(d)

    class_name = QuerySelectField(
        label='班级：',
        query_factory=query_factory,
        get_pk=get_pk,
        allow_blank=True,
        validators = [
            DataRequired("请选择班级")
        ]
    )

    name = StringField(
        label="姓名：",
        validators=[
            DataRequired("请输入姓名")
        ],
        description="姓名",
        render_kw={

            "class": "form-control",
            "id": "name",
            "placeholder": "请输入你的姓名！"
        }
    )
    sex = StringField(
        label="性别：",
        validators=[
            DataRequired("请输入你的性别")
        ],
        description="性别",
        render_kw={
            "class": "form-control",
            "id": "sex",
            "placeholder": "请输入性别！"
        }
    )
    age = StringField(
        label="年龄：",
        validators=[
            DataRequired("请输入你的年龄")
        ],
        description="年龄",
        render_kw={
            "class": "form-control",
            "id": "age",
            "placeholder": "请输入你的年龄"
        }
    )
    card = StringField(
        label="身份证证号：",
        validators=[
            DataRequired("请输入身份证")
        ],
        description="身份证",
        render_kw={
            "class": "form-control",
            "id": "card",
            "placeholder": "请输入身份证证号！"
        }
    )
    phone = StringField(
        label="手机号码：",
        validators=[
            DataRequired("请输入手机号码")
        ],
        description="手机号码",
        render_kw={
            "class": "form-control",
            "id": "phone",
            "placeholder": "请输入手机号码！"
        }
    )
    qq = StringField(
        label="qq号码：",
        validators=[
            DataRequired("请输入qq号码")
        ],
        description="qq号码",
        render_kw={
            "class": "form-control",
            "id": "qq",
            "placeholder": "请输入qq号码！"
        }
    )
    email = StringField(
        label="邮箱地址：",
        validators=[
            DataRequired("请输入邮箱地址")
        ],
        description="邮箱地址",
        render_kw={
            "class": "form-control",
            "id": "email",
            "placeholder": "请输入邮箱地址！"
        }
    )
    education = StringField(
        label="学历：",
        validators=[
            DataRequired("请输入学历")
        ],
        description="学历",
        render_kw={
            "class": "form-control",
            "id": "education",
            "placeholder": "请输入学历！"
        }
    )
    school = StringField(
        label="毕业学校：",
        validators=[
            DataRequired("请输入毕业学校")
        ],
        description="毕业学校",
        render_kw={
            "class": "form-control",
            "id": "school",
            "placeholder": "请输入毕业学校！"
        }
    )
    specialty = StringField(
        label="本人所读专业：",
        validators=[
            DataRequired("请输入所读专业")
        ],
        description="专业",
        render_kw={
            "class": "form-control",
            "id": "specialty",
            "placeholder": "请输入所读专业！"
        }
    )
    family = StringField(
        label="家庭联系人：",
        validators=[
            DataRequired("请输入家庭联系人")
        ],
        description="家庭联系人",
        render_kw={
            "class": "form-control",
            "id": "family",
            "placeholder": "请输入家庭联系人！"
        }
    )
    familyphone = StringField(
        label="联系人号码：",
        validators=[
            DataRequired("请输入联系人号码")
        ],
        description="联系人号码",
        render_kw={
            "class": "form-control",
            "id": "familyphone",
            "placeholder": "请输入联系人号码！"
        }
    )
    guangzhouadd = StringField(
        label="现广州住址：",
        validators=[
            DataRequired("请输入广州住址")
        ],
        description="现广州住址",
        render_kw={
            "class": "form-control",
            "id": "guangzhouadd",
            "placeholder": "请输入住址！"
        }
    )
    familyadd = StringField(
        label="家庭地址：",
        validators=[
            DataRequired("请输入家庭住址")
        ],
        description="家庭地址",
        render_kw={
            "class": "form-control",
            "id": "familyadd",
            "placeholder": "请输入住址！"
        }
    )
    apply = TextAreaField(
        label="报名渠道：",
        validators=[
            DataRequired("如：网络营销号，老学员介绍，来电咨询，上门咨询，校门市场，校园广告等等")
        ],
        description="版名渠道",
        render_kw={
            "class": "form-control",
            "id": "apply",
            "placeholder": "如：网络营销号，老学员介绍，来电咨询，上门咨询，校门市场，校园广告等等"
        }
    )

    submit = SubmitField(
        "提交",
        render_kw={
            "class": "btn btn-primary",
        }
    )
