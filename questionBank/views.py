import os
import time

from flask import request, url_for, flash, render_template, make_response, send_from_directory, current_app
from flask_ckeditor import upload_fail, upload_success
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash

from questionBank import app, db
from questionBank.models import User, Teacher, Question
from questionBank.commons import grades, classnums, subject_lists, subject_category_dict, QuestionTypes
from questionBank.forms import QuestionForm


@app.route('/studentRegister', methods=['GET', 'POST'])
def student_register():
    """
        if post register and goto login page
        if get go to register page
    """

    if request.method == 'GET':
        return render_template('student_register.html', grades=grades, classnums=classnums)
    else:
        student_num = request.form.get('student_num')
        name = request.form.get('name')
        grade = request.form.get('grade')
        class_num = request.form.get('class_num')
        password = request.form.get('password')
        password_hash = generate_password_hash(password)
        user = User(
            student_num=student_num, name=name, grade=grade,
            class_num=class_num, password_hash=password_hash,
            correct_list=[], wrong_list=[]
        )
        db.session.add(user)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('student_login'))


@app.route('/', methods=['GET', 'POST'])
def student_login():
    """
        used for login student
    :return:
    """
    if request.method == 'GET':
        return render_template('student_login.html')
    else:
        student_num = request.form.get('student_num')
        password = request.form.get('password')
        login_user = User.query.filter_by(student_num=student_num).first()
        if login_user != None and login_user.validate_password(password):
            return redirect(url_for('student_index'))
        else:
            flash("password error or not registered ~")
            return redirect(url_for('student_login'))


@app.route('/student_index', methods=['GET'])
def student_index():
    """
    待实现的业务逻辑： 学生端主页面
    :return:
    """
    return render_template('student_index.html')


@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    """
        used for login teacher
    :return:
    """
    if request.method == 'GET':
        return render_template('teacher_login.html')
    else:
        teacher_name = request.form.get('teacher_name')
        password = request.form.get('password')
        login_teacher = Teacher.query.filter_by(teacher_name=teacher_name).first()
        if login_teacher is not None and login_teacher.validate_password(password):
            resp = make_response(render_template('teacher_index.html'))
            subject = login_teacher.subject
            resp.set_cookie('teacher', teacher_name)
            resp.set_cookie('subject', subject)
            return resp
        else:
            flash("{}'s {} password error or not registered ~".format(teacher_name, password))
            return render_template('teacher_login.html')


# @app.route('/teacher_register', methods=['GET', 'POST'])
# def teacher_register():
#     if request.method == 'GET':
#         return  render_template('teacher_register.html', grades=grades, classnums=classnums,
#                                 subject_lists=subject_lists)
#     else:


@app.route('/add_question_pre', methods=['GET', 'POST'])
def add_question_pre():
    """
    题目类型和数量选择
    :return:
    """
    if request.method == "GET":
        subject = request.cookies.get("subject")
        subject_category = subject_category_dict[subject]
        return render_template('question_modified_pages/question_add_pre.html', subject=subject,
                               subject_category=subject_category, question_types=QuestionTypes)
    else:
        category = request.form.get('category')
        question_type = request.form.get('question_type')
        question_num = int(request.form.get('question_num'))
        question_form = QuestionForm()
        return render_template('question_modified_pages/question_add.html', category=category,
                               question_type=question_type, question_num=question_num, form=question_form)


@app.route('/add_question/', methods=['GET', 'POST'])
def add_question():
    """
    新增题目
    :return:
    """
    if request.method == 'GET':
        subject = request.cookies.get('subject')
        subject_category = subject_category_dict[subject]
        question_form = QuestionForm()
        question_form.set_question_category(list(zip(subject_category, subject_category)))
        return render_template('question_modified_pages/question_add.html', form=question_form)
    else:
        category = request.form.get('category')
        question = request.files['file']
        base_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base_path, 'static', app.config['UPLOAD_FOLDER'], category)
        if not os.path.exists(path):
            os.mkdir(path)
        file_name = secure_filename(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))
        question.save(os.path.join(path, file_name))
        subject = request.cookies.get('subject')
        question = "{}.{}".format(category, file_name)
        # question_num = int(request.form.get('question_num'))
        answer = {}
        grade = {}
        for i in range(int(question_num)):
            answer['第{}题'.format(i + 1)] = request.form.get('question_answer_%d'.format(i + 1))
            grade['第{}题'.format(i + 1)] = request.form.get('question_grade_%d'.format(i + 1))
        question = Question(
            belong_subject=subject, category=category, question_type=question_type,
            question=question, answer=answer, grade=grade
        )
        db.session.add(question)
        db.session.commit()
        flash('question created~')
        return render_template('teacher_index.html')


@app.route('/static/upload/<filename>')   # this place is used for the url in the ckeditor textbox
def uploaded_files(filename):
    path = os.path.join(current_app.name, 'static', current_app.config['CKEDITOR_FILE_UPLOADER'])
    return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')  # 获取上传图片文件对象
    # Add more validations here
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:  # 验证文件类型示例
        return upload_fail(message='Image only!')  # 返回upload_fail调用
    upload_path = os.path.join(current_app.name, 'static', current_app.config['CKEDITOR_FILE_UPLOADER'])
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    f.save(os.path.join(upload_path, f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)    # 返回upload_success调用