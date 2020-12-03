from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from questionBank import db
from questionBank.commons import grades, classnums

# grades = ("高{}".format(grade+1) for grade in range(3))
# classnums = ("{}班".format(classnum+1) for classnum in range(16))


# 模型类
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.String(20))
    name = db.Column(db.String(20))
    grade = db.Column(db.String(2))
    class_num = db.Column(db.String(3))
    password_hash = db.Column(db.String(128))  # 密码散列值
    correct_list = db.Column(db.PickleType)
    wrong_list = db.Column(db.PickleType)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    subject = db.Column(db.String(10))
    class_teaching = db.Column(db.PickleType)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


