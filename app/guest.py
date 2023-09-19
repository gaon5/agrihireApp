from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
from app import app, check_permissions, operate_sql, bcrypt, scheduler, region_list, title_list, city_list, question_list


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
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        account = operate_sql("""SELECT user_id,is_admin,is_customer,is_staff,is_root,password FROM user_account WHERE email=%s;""", (email,), fetch=0)
        if account is not None:
            if bcrypt.check_password_hash(account[5], password):
                # Login successful
                session['loggedIn'] = True
                session['user_id'] = account[0]
                session['is_admin'] = account[1]
                session['is_customer'] = account[2]
                session['is_staff'] = account[3]
                session['is_root'] = account[4]
                msg = 'Login successful'
                return render_template('guest/jump.html', goUrl='/', msg=msg)
        # username or password error
        msg = 'username or password error.'
    return render_template('guest/login.html', msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedIn', None)
    session.pop('user_id', None)
    session.pop('is_admin', None)
    session.pop('is_customer', None)
    session.pop('is_staff', None)
    session.pop('is_root', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    today = datetime.today().date()
    if request.method == 'POST':
        # Get data
        email = request.form.get('email')
        password = request.form.get('password')
        given_name = request.form.get('given_name')
        surname = request.form.get('surname')
        title = request.form.get('title')
        question = request.form.get('question')
        answer = request.form.get('answer')
        account = operate_sql("""SELECT email FROM user_account WHERE email = %s;""", (email,), fetch=0)
        if account:
            # Email already exists
            msg = 'Email already exists!'
            return render_template('guest/register.html', msg=msg, titles=title_list, questions=question_list)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Insert account data into database
        operate_sql("""INSERT INTO user_account (email, password, is_customer, register_date, last_login_date) 
                                    VALUES (%s, %s, 1, %s, %s)""", (email, hashed_password, today, today))
        user_id = operate_sql("""SELECT user_id from user_account WHERE email=%s;""", (email,), fetch=0)
        value = (user_id[0], title, given_name, surname, question, answer)
        operate_sql("""INSERT INTO customer (user_id,title_id,first_name,last_name,question_id,answer,state) VALUES (%s,%s,%s,%s,%s,%s,1);""", value)
        account = operate_sql("""SELECT user_id,is_admin,is_customer,is_staff,is_root FROM user_account WHERE user_id=%s;""", (user_id[0],), fetch=0)
        session['loggedIn'] = True
        session['user_id'] = account[0]
        session['is_admin'] = account[1]
        session['is_customer'] = account[2]
        session['is_staff'] = account[3]
        session['is_root'] = account[4]
        msg = 'Registration success!'
        return render_template('guest/jump.html', goUrl='/', msg=msg)
    return render_template('guest/register.html', titles=title_list, questions=question_list)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    msg = ''
    email = request.args.get('email')
    if email:
        account = operate_sql("""SELECT user_id FROM user_account WHERE email=%s AND is_customer=1;""", (email,), fetch=0)
        if not account:
            msg = "Didn't have this account!"
            return render_template('guest/reset_password.html', msg=msg)
        else:
            session['user_id'] = account[0]
            question = operate_sql("""SELECT sq.question_id,sq.question FROM customer AS c 
                LEFT OUTER JOIN security_question sq on sq.question_id = c.question_id WHERE user_id=%s;""", (account[0],), fetch=0)
            return render_template('guest/answer.html', question=question)
    if request.method == 'POST':
        # Get data
        user_id = session['user_id']
        answer = request.form.get('answer')
        question = operate_sql("""SELECT answer FROM customer WHERE user_id=%s;""", (user_id,), fetch=0)
        if answer.lower() == question[0].lower():
            return redirect(url_for('change_password'))
        else:
            msg = "The answer is incorrect!"
        return render_template('guest/answer.html', question=question, msg=msg)
    return render_template('guest/reset_password.html', msg=msg)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user_id = session['user_id']
    if request.method == 'POST':
        session.pop('user_id', None)
        password = request.form.get('password')
        user_id = request.form.get('user_id')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        operate_sql("""UPDATE user_account SET password=%s WHERE user_id=%s;""", (hashed_password, user_id,))
        return redirect(url_for('login'))
    return render_template('guest/change_password.html', user_id=user_id)


@app.route('/change_information', methods=['GET', 'POST'])
def change_information():
    return render_template('guest/change_information.html')


# @app.errorhandler(Exception)
# def handle_error(error):
#     """
#     Receive all unexpected errors
#     :param error:
#     :return: error.html
#     """
#     print(error)
#     return render_template('guest/error.html', permissions=check_permissions())
