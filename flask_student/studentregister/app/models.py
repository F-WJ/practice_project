# _*_ coding: utf-8 _*_
__author__ = 'FWJ'
__date__ = 2017 / 12 / 24
from app import db



class StudentMessage(db.Model):
    __tablename__ = "studentmessage"
    id = db.Column(db.Integer, primary_key=True)  # 序号
    name = db.Column(db.String(100))  # 姓名
    sex = db.Column(db.String(100))  # 性别
    age = db.Column(db.String(100))  # 年龄
    card = db.Column(db.String(100))  # 身份证
    phone = db.Column(db.String(100))  # 手机号码
    qq = db.Column(db.String(100))  # qq号
    email = db.Column(db.String(100))  # 邮箱
    education = db.Column(db.String(100))  # 学历
    school = db.Column(db.String(100))  # 毕业学校
    specialty = db.Column(db.String(100))  # 专业
    family = db.Column(db.String(100))  # 家庭联系人
    familyphone = db.Column(db.String(100))  # 家庭联系人电话
    guangzhouadd = db.Column(db.Text)  # 广州地址
    familyadd = db.Column(db.Text)  # 家庭地址
    apply = db.Column(db.Text)  # 报名渠道
    class_id = db.Column(db.Integer, db.ForeignKey('classname.id'))  # 班级

    def __repr__(self):
        return "<StudentMessage %r>" % self.name


# 班级信息
class ClassName(db.Model):
    __tablename__ = "classname"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    class_excel = db.Column(db.Integer, default=0)        # 检查excel是否存在
    student_name = db.relationship("StudentMessage", backref='classname')

    def __repr__(self):
        return "<ClassName %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100), unique=True)  # 管理员密码

    def __repr__(self):
        return "<Admin %r>" % self.name

    # 验证哈希
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# #
if __name__ == "__main__":
    # 创建数据表
    db.create_all()
    # 添加管理员
    # 生成哈希密码
    from werkzeug.security import generate_password_hash
    admin = Admin(
        name="admin",
        pwd=generate_password_hash("kumanjin@student"),
    )
    db.session.add(admin)
    db.session.commit()
