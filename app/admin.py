from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import re
import bcrypt
from app import app, check_permissions, scheduler, sql_function

# route for update information
@app.route('/admin_update_personal_information', methods=['GET','POST'])
def admin_update_personal_information():
    # get user_id from session
    # user_id = session["user_id"]
    user_id = 1
    # create message variables to display in templates
    error_msg = ''
    msg = ''
    # update personal information if user submits the form
    if request.method == 'POST':
        first_name = request.form.get('first_name').capitalize()
        last_name = request.form.get('last_name').capitalize()
        title = int(request.form.get('title'))
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        user_id = int(request.form.get('user_id'))
        email_result = sql_function.get_email(email)
        if int(email_result['user_id']) != user_id:
            error_msg = "Email entered is already in use. Please enter another email address."
        else:
            sql_function.update_admin_details(first_name, last_name, title, phone_number, email, user_id)
            msg = "Update successful"
    # take latest details_list
    details_list = sql_function.get_admin_details(user_id)
    title_list = sql_function.title_list
    return render_template('admin/update_personal_information.html', details_list=details_list, title_list=title_list, msg=msg, error_msg=error_msg)

# route for changing password
@app.route('/admin_change_password', methods=['GET','POST'])
def admin_change_password():
    # get user_id from session
    # user_id = session["user_id"]
    user_id = 1
    # create message variables to display in templates
    error_msg = ""
    msg = ""
    # get old password from user
    original_password = sql_function.get_password(user_id)['password'].encode('utf-8')
    # update password if the user submits the form
    if request.method == 'POST':
        old_password = request.form.get('old_pw')
        new_password = request.form.get('new_pw')
        # convert passwords into bytes
        byte_old_password = old_password.encode('utf-8')
        byte_new_password = new_password.encode('utf-8')
        # check whether the old password is correct
        if not bcrypt.checkpw(byte_old_password, original_password):
            error_msg = "Incorrect old password. Please try again."
        # check whether the passwords are the same
        elif bcrypt.checkpw(byte_new_password, original_password):
            error_msg = "New password cannot be the same as previous password. Please try again"
        # if not, update hashed password
        else:
            hashed_password = bcrypt.hashpw(byte_new_password, bcrypt.gensalt())
            sql_function.update_password(hashed_password, user_id)
            msg = "Password changed."
    return render_template('admin/change_password.html', msg=msg, error_msg=error_msg)