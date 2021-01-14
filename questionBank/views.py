import os
import time

from flask import request, url_for, flash, render_template, make_response, send_from_directory, current_app, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash

from questionBank import app, db
from questionBank.models import User, Teacher, Question
from questionBank.commons import grades_list, classnums_list, subject_lists, subject_category_dict, QuestionTypes, \
    gen_rnd_filename, question_types
from questionBank.forms import QuestionForm


@app.route('/studentRegister', methods=['GET', 'POST'])
def student_register():
    """
        if post register and goto login page
        if get go to register page
    """

    if request.method == 'GET':
        grades = grades_list
        classnums = classnums_list
        return render_template('student_pages/student_register.html', grades=grades, classnums=classnums)
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
        return render_template('student_pages/student_login.html')
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
    return render_template('student_pages/student_index.html')


@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    """
        used for login teacher
    :return:
    """
    if request.method == 'GET':
        return render_template('teacher_pages/teacher_login.html')
    else:
        teacher_name = request.form.get('teacher_name')
        password = request.form.get('password')
        login_teacher = Teacher.query.filter_by(teacher_name=teacher_name).first()
        if login_teacher is not None and login_teacher.validate_password(password):
            resp = make_response(render_template('teacher_pages/teacher_index.html'))
            subject = login_teacher.subject
            resp.set_cookie('teacher', teacher_name)
            resp.set_cookie('subject', subject)
            return resp
        else:
            flash("{}'s {} password error or not registered ~".format(teacher_name, password))
            return render_template('teacher_pages/teacher_login.html')


@app.route('/teacher/logout', methods=['GET', 'POST'])
def teacher_logout():
    return redirect(url_for('teacher_login'))


@app.route('/student/logout', methods=['GET', 'POST'])
def student_logout():
    return redirect(url_for('student_login'))


# @app.route('/teacher_register', methods=['GET', 'POST'])
# def teacher_register():
#     if request.method == 'GET':
#         return  render_template('teacher_register.html', grades=grades, classnums=classnums,
#                                 subject_lists=subject_lists)
#     else:


@app.route('/add_question/<question_num>', methods=['GET', 'POST'])
def add_question(question_num):
    """
    新增题目
    :return:
    """
    if request.method == 'GET':
        subject = request.cookies.get('subject')
        subject_category = subject_category_dict[subject]
        question_form = QuestionForm()
        question_form.set_question_category(list(zip(subject_category, subject_category)))
        question_form.set_question_type(list(zip(question_types, question_types)))
        return render_template('question_modified_pages/question_add.html', form=question_form)
    else:
        question_category = request.form.get('question_category')
        question_type = request.form.get('question_type')
        question_body = request.form.get('question_body')
        subject = request.cookies.get('subject')
        if int(question_num) > 1:
            question_type = question_types[0]
        else:
            question_type = question_type[1]
        for i in range(int(question_num)):
            answer = {"第{}小题".format(i+1): request.form.get('answer{}'.format(i+1))}
            grade = {"第{}小题".format(i+1): 2}

        question = Question(
            belong_subject=subject, category=question_category, question_type=question_type,
            question=question_body, answer=answer, grade=grade
        )
        db.session.add(question)
        db.session.commit()
        flash('question created~')
        return render_template('teacher_pages/teacher_index.html')


@app.route('/imageuploader/<category>', methods=['POST'])
def imageuploader(category):
    file = request.files.get('file')
    if file:
        filename = file.filename.lower()
        extension = filename.split('.')[-1]
        if extension in ['jpg', 'gif', 'png', 'jpeg']:
            fullpath = os.path.join(current_app.name, 'static', app.config['UPLOADED_PATH'], category)
            filename = "{}.{}".format(gen_rnd_filename(), extension)
            img_file = os.path.join(fullpath, filename)
            if not os.path.exists(fullpath):
                os.makedirs(fullpath)
            file.save(img_file)
            filepath = os.path.join('/static', app.config['UPLOADED_PATH'], category, filename)
            return jsonify({'location' : filepath})

    # fail, image did not upload
    output = make_response(404)
    output.headers['Error'] = 'Image failed to upload'
    return output


@app.route('/add_lession', methods=['GET', 'POST'])
def add_lession():
    return render_template('lession_pages/add_lession.html')


@app.route('/student/practice_modified', methods=['GET', 'POST'])
def student_practice_modified():
    if request.method == 'GET':
        subjects = subject_lists
        return render_template('practice_pages/practice_config.html', subject_lists=subjects)
    else:
        pass


@app.route('/student/general_practice')
def student_general_practice():
    if request.method == 'GET':
        return render_template('practice_pages/general_practice.html')


@app.route('/student/special_practice')
def student_special_practice():
    if request.method == 'GET':
        return render_template('practice_pages/special_practice.html')
