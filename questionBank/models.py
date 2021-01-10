from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from questionBank import db



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


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    belong_subject = db.Column(db.String(10))
    category = db.Column(db.String(20))
    question_type = db.Column(db.String(10))
    question = db.Column(db.PickleType)
    answer = db.Column(db.PickleType)  # 以字典形式存储，key为小题号，value为具体答案值
    grade = db.Column(db.PickleType)

    def get_grade(self, answer):
        pass