import os
import time
from random import choice, randint

from flask import request, url_for, flash, render_template, make_response, send_from_directory, current_app, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash

from questionBank import app, db
from questionBank.models import User, Teacher, Question
from questionBank.commons import grades_list, classnums_list, subject_lists, subject_category_dict, QuestionTypes, \
    gen_rnd_filename, question_types, DEFAULT_SUBJECT, DEFAULT_QUESTION_NUM, LOWER_BOUND
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
        user = User.query.filter_by(student_num=student_num).first()
        if user is not None and user.validate_password(password):
            resp = make_response(redirect(url_for('student_index')))
            resp.set_cookie('user', str(user.id))
            return resp
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


@app.route('/add_question/<question_num>/<question_type>', methods=['GET', 'POST'])
def add_question(question_num, question_type):
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
        question_body = request.form.get('question_body')
        subject = request.cookies.get('subject')
        answer = {}
        grade = {}
        for i in range(int(question_num)):
            answer["第{}小题".format(i+1)] = ''.join(request.form.getlist('answer{}'.format(i+1)))
            grade["第{}小题".format(i+1)] = 2
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
        return render_template('practice_pages/practice_config.html')
    else:
        pass


@app.route('/student/special_practice_modified', methods=['GET', 'POST'])
def student_special_practice_modified():
    """
    config for special practice
    :param category_num:
    :return:
    """
    if request.method == 'GET':
        subject = DEFAULT_SUBJECT
        categories = subject_category_dict[subject]
        return render_template('practice_pages/special_practice_config.html', subject_category=categories)
    else:
        question_config = {}
        category_list = request.form.getlist('category')
        for i in range(len(category_list)):
            question_category_name = category_list[i]
            question_category_num = request.form.get('question_num_{}'.format(int(question_category_name[:2])))
            question_config[question_category_name] = question_category_num
        return redirect(url_for('student_special_practice', question_config=question_config))


@app.route('/student/general_practice', methods=['GET', 'POST'])
def student_general_practice():
    """
    随机从题库中抽取题目
    :return:
    """
    total_question_num = Question.query.count()
    question_num = DEFAULT_QUESTION_NUM if DEFAULT_QUESTION_NUM <= total_question_num else total_question_num
    if request.method == 'GET':
        question_list = []
        if total_question_num <= LOWER_BOUND:  # 总问题数太少时
            total_offset_list = [i for i in range(total_question_num)]
            for i in range(question_num):

                offset_num = choice(total_offset_list)
                question_list.append(Question.query.offset(offset_num).first())
                total_offset_list.remove(offset_num)
        else:  # 总问题数不少时
            offset_list = []
            for i in range(question_num):
                offset_num = randint(0, total_question_num - 1)
                while offset_num in offset_list:
                    offset_num = randint(0, total_question_num - 1)
                offset_list.append(offset_num)
                question_list.append(Question.query.offset(offset_num).first())
        resp = make_response(render_template('practice_pages/general_practice.html', question_list = question_list))
        for i in range(len(question_list)):
            question = question_list[i]
            resp.set_cookie("question_{}".format(i+1), str(question.id))
        return resp
    else:
        login_id = int(request.cookies.get('user'))
        user = User.query.filter_by(id=login_id).first()
        grade = 0
        for i in range(question_num):
            question_id = int(request.cookies.get('question_{}'.format(i+1)))
            question = Question.query.filter_by(id=question_id).first()
            user_answer = {}
            for k in range(len(question.question_type)):
                user_answer['第{}小题'.format(k+1)] = ''.join(request.form.getlist('user_answer_{}_{}'.format(i+1, k+1)))
            grade += question.get_grade(user_answer)
            if question.is_correct(user_answer):
                user.add_correct_list(question_id)
            else:
                user.add_wrong_list(question_id)
        db.session.commit()
        return render_template('practice_pages/show_result.html', grade=grade, user=user)


@app.route('/special_practice/<dict:question_config>', methods=['GET', 'POST'])
def student_special_practice(question_config):
    """
    jump to special practice page
    :return:
    """
    if request.method == 'GET':
        question_list = []
        lower_bund = 20
        for question_category in question_config.keys():
            question_num = int(question_config[question_category])
            questions = Question.query.filter_by(category=question_category)
            total_question_num = questions.count()
            question_num = question_num if question_num < total_question_num else total_question_num
            if total_question_num <= lower_bund:  # 总问题数太少时
                total_offset_list = [i for i in range(total_question_num)]
                for i in range(question_num):
                    offset_num = choice(total_offset_list)
                    question_list.append(questions.offset(offset_num).first())
                    total_offset_list.remove(offset_num)
            else:  # 总问题数不少时
                offset_list = []
                for i in range(question_num):
                    offset_num = randint(0, questions.count()-1)
                    while offset_num in offset_list:
                        offset_num = randint(0, questions.count() - 1)
                    offset_list.append(offset_num)
                    question_list.append(questions.offset(offset_num).first())
        resp = make_response(render_template('practice_pages/special_practice.html', question_list = question_list, question_config=question_config))
        for i in range(len(question_list)):
            question = question_list[i]
            resp.set_cookie("question_{}".format(i+1), str(question.id))
        return resp
    else:
        login_id = int(request.cookies.get('user'))
        user = User.query.filter_by(id=login_id).first()
        i = 1
        grade = 0
        for question_category in question_config.keys():
            question_num = int(question_config[question_category])
            user_answer = {}
            for j in range(question_num):
                question_id = int(request.cookies.get('question_{}'.format(i)))
                question = Question.query.filter_by(id=question_id).first()
                for k in range(len(question.question_type)):
                    user_answer['第{}小题'.format(k+1)] = request.form.get('user_answer_{}_{}'.format(i, k+1))
                grade += question.get_grade(user_answer)
                if question.is_correct(user_answer):
                    user.add_correct_list(question_id)
                else:
                    user.add_wrong_list(question_id)
                i += 1
        db.session.commit()
        return render_template('practice_pages/show_result.html', grade=grade, user=user)