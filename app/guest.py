from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
from app import app, check_permissions, select_sql, bcrypt, scheduler


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
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        account = select_sql("""SELECT * FROM user_account WHERE username = %s;""", (username,))
        if account is not None:
            if bcrypt.check_password_hash(account[3], password):
                # Login successful
                return redirect(url_for('index'))
        # username or password error
    return render_template('guest/login.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    today = datetime.today().date()
    if request.method == 'POST':
        # Get data
        username = request.form.get('username')
        password = request.form.get('password')
        account = select_sql("""SELECT email, username FROM user_account WHERE email = %s OR username = %s', (email, username,));""",
                             (username, username,), fetch=0)
        if account:
            # Username or email already exists
            return render_template('guest/register.html')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Insert account data into database
        return redirect(url_for('index'))
    return render_template('guest/register.html')


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    return render_template('guest/change_password.html')


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
