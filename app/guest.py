from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
from app import app, check_permissions, select_sql


@app.route('/')
def index():
    return render_template('guest/index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('guest/login.html')


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
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
