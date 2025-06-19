from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Task
from app.forms import LoginForm, RegistrationForm, TaskForm
from datetime import datetime
from flask import Blueprint
from flask import abort

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, 
                   description=form.description.data,
                   author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been added!')
        return redirect(url_for('main.tasks'))
    
    tasks = current_user.tasks.order_by(Task.timestamp.desc()).all()
    return render_template('tasks.html', title='Tasks', form=form, tasks=tasks)

@main.route('/complete_task/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    task.completed = True
    db.session.commit()
    flash('Task marked as completed!')
    return redirect(url_for('main.tasks'))

@main.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!')
    return redirect(url_for('main.tasks'))

@main.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        db.session.commit()
        flash('Task updated!')
        return redirect(url_for('main.tasks'))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
    return render_template('edit_task.html', title='Edit Task', form=form)
