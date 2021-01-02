from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, FileField, SubmitField, SelectField


class QuestionForm(FlaskForm):
    question_category = SelectField('类别', choices=[()])
    question_body = CKEditorField('编辑题目')

    def set_question_category(self, category):
        self.question_category.choices = category
