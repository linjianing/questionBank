# 自定义命令
import click

from questionBank import app, db
from questionBank.models import Teacher


@app.cli.command()
@click.option('--teacher_name', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
@click.option('--subject', prompt=True, help='The subject to teach.')
@click.option('--classes', prompt=True, help='Classes to teach.')
def add_teacher(teacher_name, password, subject=None, classes=None):
    """Create user."""
    db.create_all()
    teacher = Teacher.query.filter_by(teacher_name=teacher_name).first()
    if teacher is not None:
        click.echo('Updating teacher_account...')
        teacher.set_password(password)
    else:
        click.echo('Creating teacher_account...')
        teacher = Teacher(teacher_name=teacher_name, subject=subject, class_teaching=classes)
        teacher.set_password(password)
        db.session.add(teacher)

    db.session.commit()
    click.echo('Done.')