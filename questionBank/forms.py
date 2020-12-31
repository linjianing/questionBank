from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, FileField, SubmitField


class QuestionForm(FlaskForm):
    title = StringField('Title')
    question_body = CKEditorField('Body')
    submit = SubmitField('Submit')
