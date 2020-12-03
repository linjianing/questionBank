from flask import request, url_for, flash, render_template
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash

from questionBank import app, db
from questionBank.models import User, Teacher
from questionBank.commons import grades, classnums, subject_lists


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
        if login_teacher != None and login_teacher.validate_password(password):
            return redirect('teacher_index.html')
        else:
            flash('password error or not registered ~')
            return render_template('teacher_login.html')


@app.route('/teacher_register', methods=['GET', 'POST'])
def teacher_register():
    if request.method == 'GET':
        return  render_template('teacher_register.html', grades=grades, classnums=classnums,
                                subject_lists=subject_lists)
    else:

