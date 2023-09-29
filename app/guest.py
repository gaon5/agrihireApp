from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import re
from app import app, check_permissions, scheduler, bcrypt, sql_function


@app.route('/my_task')
@scheduler.task('interval', id='my_task', seconds=60)
def my_task():
    """
    This is a scheduled task
    :return:
    """
    pass


@app.route('/')
def index():
    return render_template('guest/index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    breadcrumbs = [{"text": "Login", "url": "/login/"}]
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        account = sql_function.get_account(email)
        if account is not None:
            if bcrypt.check_password_hash(account['password'], password):
                # Login successful
                sql_function.set_last_login_date(account['user_id'])
                session['loggedIn'] = True
                session['user_id'] = account['user_id']
                session['is_admin'] = account['is_admin']
                session['is_customer'] = account['is_customer']
                session['is_staff'] = account['is_staff']
                msg = 'Login successful'
                return render_template('guest/jump.html', goUrl='/', msg=msg)
        # username or password error
        msg = 'username or password error.'
    return render_template('guest/login.html', msg=msg, breadcrumbs=breadcrumbs)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedIn', None)
    session.pop('user_id', None)
    session.pop('is_admin', None)
    session.pop('is_customer', None)
    session.pop('is_staff', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    breadcrumbs = [{"text": "Register", "url": "/register"}]
    if request.method == 'POST':
        # Get data
        email = request.form.get('email')
        password = request.form.get('password')
        given_name = request.form.get('given_name')
        surname = request.form.get('surname')
        title = request.form.get('title')
        question = request.form.get('question')
        answer = request.form.get('answer')
        account = sql_function.get_account(email)
        if account:
            # Email already exists
            msg = 'Email already exists!'
            return render_template('guest/register.html', msg=msg, titles=sql_function.title_list, questions=sql_function.question_list, breadcrumbs=breadcrumbs)
        # Insert account data into database
        account = sql_function.register_account(email, password, title, given_name, surname, question, answer)
        session['loggedIn'] = True
        session['user_id'] = account['user_id']
        session['is_admin'] = account['is_admin']
        session['is_customer'] = account['is_customer']
        session['is_staff'] = account['is_staff']
        msg = 'Registration success!'
        return render_template('guest/jump.html', goUrl='/', msg=msg)
    return render_template('guest/register.html', titles=sql_function.title_list, questions=sql_function.question_list, breadcrumbs=breadcrumbs)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    msg = ''
    breadcrumbs = [{"text": "Reset Password", "url": "/reset_password"}]
    email = request.args.get('email')
    if email:
        account = sql_function.get_account(email)
        if not account:
            msg = "Didn't have this account!"
            return render_template('guest/reset_password.html', msg=msg, breadcrumbs=breadcrumbs)
        else:
            session['user_id'] = account['user_id']
            question = sql_function.get_customer_question(account['user_id'])
            return render_template('guest/answer.html', question=question, breadcrumbs=breadcrumbs)
    if request.method == 'POST':
        # Get data
        user_id = session['user_id']
        answer = request.form.get('answer')
        question = sql_function.get_customer_question(user_id)
        if answer.lower() == question['answer'].lower():
            return redirect(url_for('change_password'))
        else:
            msg = "The answer is incorrect!"
        return render_template('guest/answer.html', question=question, msg=msg, breadcrumbs=breadcrumbs)
    return render_template('guest/reset_password.html', msg=msg, breadcrumbs=breadcrumbs)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user_id = session['user_id']
    breadcrumbs = [{"text": "Change Password", "url": "/change_password"}]
    if request.method == 'POST':
        session.pop('user_id', None)
        password = request.form.get('password')
        user_id = request.form.get('user_id')
        sql_function.set_password(password, user_id)
        return redirect(url_for('login'))
    return render_template('guest/change_password.html', user_id=user_id, breadcrumbs=breadcrumbs)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}]
    # First determine whether to log in, then determine the user type, and then return different panels according to the type.
    return render_template('admin/dashboard.html', breadcrumbs=breadcrumbs)
    return render_template('staff/dashboard.html', breadcrumbs=breadcrumbs)
    return redirect(url_for('index'))


@app.route('/edit_detail', methods=['GET', 'POST'])
def edit_detail():
    breadcrumbs = [{"text": "Edit My Detail", "url": "/edit_detail"}]
    # First determine whether to log in, then determine the user type, and then query the database based on the type.
    return render_template('admin/edit_detail.html', breadcrumbs=breadcrumbs)
    return render_template('staff/edit_detail.html', breadcrumbs=breadcrumbs)
    return render_template('customer/edit_detail.html', breadcrumbs=breadcrumbs)


# @app.errorhandler(Exception)
# def handle_error(error):
#     """
#     Receive all unexpected errors
#     :param error:
#     :return: error.html
#     """
#     print(error)
#     return render_template('guest/error.html', permissions=check_permissions())
