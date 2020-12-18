from flask_wtf import form, validators
from wtforms import StringField, FileField


class QuestionForm(form):
    category = StringField('类别', [validators.length(max=20)])
    question = FileField('选择题目（图片形式）', [validators])