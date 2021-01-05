from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    question_category = SelectField('类别', choices=[()])
    question_type = SelectField('题型', choices=[()])
    question_body = TextAreaField('编辑题目')
    submit = SubmitField('提交题目')

    def set_question_category(self, categories):
        self.question_category.choices = categories

    def set_question_type(self, types):
        self.question_type.choices = types
