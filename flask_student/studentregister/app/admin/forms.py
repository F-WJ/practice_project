# _*_ coding: utf-8 _*_
__author__ = 'FWJ'
__date__ = 2017 / 12 / 24
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField,form, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import ClassName, Admin


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label="账号",
        # 验证器（显示错误信息内容）
        validators=[
            DataRequired("请输入账号！")
        ],
        # 描述
        description="账号",
        # 附加选项
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            # html默认错误信息
            # "required": "required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description='密码',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            # "required": "required"
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    # 验证账号
    def validate_account(self, field):
        account = field.data
        # 查询用户是否存在，并统计
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            # 触发异常后，后面的代码就不会再执行
            raise ValidationError("账号不存在！")


# 查找班级
def query_factory():
    return [r.name for r in ClassName.query.all()]


# 班级id
def get_pk(obj):
    return ClassName.query.filter_by(name=obj).first().id


class SaveForm(FlaskForm):
        '''
        使用SelectField存在的问题

        不过严格来说，上述的场景并不是很适合用SelectField。因为在使用过程中会发现即使Task中的数据一直在更新而下拉列表框中的记录永远不变。

        主要原因是task是表单类中的一个静态成员，定义之后就保持不变。因此，即使Task表中的数据一直在变，但是tasks的结果是已经固定的。
        '''
        class_name = QuerySelectField(
            label='班级：',
            query_factory=query_factory,
            get_pk=get_pk,
            allow_blank=True,
            validators=[
                DataRequired('请选择班级')
            ],
        )
        Download = SubmitField(
            label='导入excel表',
            render_kw={
                "class": "btn btn-primary",
            }

    )


# 班级添加
class ClassAddForm(FlaskForm):
    class_add = StringField(
        label="添加班级：",
        validators=[
            DataRequired('请输入班级')
        ],
        description="添加班级",
        render_kw={
            "class": "form-control",
            "id": "class_add",
            "placeholder": "请输入班级！"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )