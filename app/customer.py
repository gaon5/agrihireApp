from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import re
from app import app, check_permissions, sql_function, bcrypt


@app.route('/equipments', defaults={'category': None, 'sub': None})
@app.route('/equipments/<category>', defaults={'sub': None})
@app.route('/equipments/<category>/<sub>')
def equipments(category, sub):
    breadcrumbs = [{"text": "Equipments", "url": "/equipments"}]
    sub_id = category_id = None
    page = request.args.get('page')
    if not page:
        sql_page = 0
    else:
        page = int(page)
        sql_page = (page - 1) * 12
    if category:
        if any(categories['name'] == category for categories in sql_function.category.values()):
            breadcrumbs.append({"text": str(category).replace("-", " "), "url": "/equipments/" + str(category)})
            category_id = next((key for key, value in sql_function.category.items() if value['name'] == category), None)
            if sub:
                if sub in sql_function.category[category_id]['subcategories']:
                    sub_id = next((item['sub_id'] for item in sql_function.sub_category_list if item['name'] == sub), None)
                    breadcrumbs.append({"text": str(sub).replace("-", " "), "url": "/equipments/" + str(category) + "/" + str(sub)})
                else:
                    msg = "Sorry, we can't find the page you're looking for!."
                    return render_template('guest/jump.html', goUrl='/', msg=msg)
        else:
            msg = "Sorry, we can't find the page you're looking for!."
            return render_template('guest/jump.html', goUrl='/', msg=msg)
    if category_id:
        if sub_id:
            sql_equipments, count = sql_function.get_equipment_by_sub(sub_id, sql_page)
        else:
            sql_equipments, count = sql_function.get_equipment_by_category(category_id, sql_page)
    else:
        sql_equipments, count = sql_function.get_all_equipment(sql_page)
    return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, category_list=sql_function.category_list,
                           count=count)


@app.route('/equipments/search_equipment', methods=['GET', 'POST'])
def search_equipment():
    breadcrumbs = [{"text": "Equipments", "url": "/equipments"}, {"text": "Search", "url": ""}]
    equipment = request.args.get('equipment')
    page = request.args.get('page')
    if not page:
        sql_page = 0
    else:
        page = int(page)
        sql_page = (page - 1) * 12
    if equipment:
        sql_equipments, count = sql_function.get_equipment_by_search(equipment, sql_page)
        return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, category_list=sql_function.category_list,
                               count=count)
    else:
        msg = "Sorry, we can't find the page you're looking for!."
        return render_template('guest/jump.html', goUrl='/', msg=msg)


@app.route('/equipments/<category>/<sub>/detail', defaults={'detail_id': None})
@app.route('/equipments/<category>/<sub>/detail/<detail_id>', methods=['GET', 'POST'])
def equipment_detail(category, sub, detail_id):
    breadcrumbs = [{"text": "Equipments", "url": "/equipments"}]
    if category:
        if any(categories['name'] == category for categories in sql_function.category.values()):
            breadcrumbs.append({"text": str(category).replace("-", " "), "url": "/equipments/" + str(category)})
            category_id = next((key for key, value in sql_function.category.items() if value['name'] == category), None)
            if sub:
                if sub in sql_function.category[category_id]['subcategories']:
                    breadcrumbs.append({"text": str(sub).replace("-", " "), "url": "/equipments/" + str(category) + "/" + str(sub)})
                else:
                    msg = "Sorry, we can't find the page you're looking for!."
                    return render_template('guest/jump.html', goUrl='/', msg=msg)
        else:
            msg = "Sorry, we can't find the page you're looking for!."
            return render_template('guest/jump.html', goUrl='/', msg=msg)
    if not detail_id:
        msg = "Sorry, we can't find the page you're looking for!."
        return render_template('guest/jump.html', goUrl='/', msg=msg)
    breadcrumbs.append({"text": "Detail", "url": ""})

    equipment = sql_function.get_equipment_by_id(detail_id)
    if request.method == 'POST':
        select_date = request.form.get('select_date')
        days = request.form.get('days')
        if select_date:
            select_date = datetime.strptime(select_date, "%d %b %Y")
            print(select_date.date())
        if days:
            start_date_str, end_date_str = map(str.strip, days.split("to"))
            start_date = datetime.strptime(start_date_str, "%d %b %Y")
            end_date = datetime.strptime(end_date_str, "%d %b %Y")
            days = (start_date - end_date).days
            print(days)
    return render_template('customer/equipment_detail.html', detail_id=detail_id, breadcrumbs=breadcrumbs, equipment=equipment)


# route for update information
@app.route('/customer_update_personal_information', methods=['GET', 'POST'])
def customer_update_personal_information():
    # get user_id from session
    # user_id = session["user_id"]
    user_id = 3
    # create message variables to display in templates
    error_msg = ''
    msg = ''
    # update personal information if user submits the form
    if request.method == 'POST':
        first_name = request.form.get('first_name').capitalize()
        last_name = request.form.get('last_name').capitalize()
        # convert string into datetime object
        birth_date = datetime.strptime(request.form.get('birth_date'), '%d %b %Y').strftime('%Y-%m-%d')
        title = int(request.form.get('title'))
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        region = int(request.form.get('region'))
        city = int(request.form.get('city'))
        street_name = request.form.get('street_name')
        user_id = int(request.form.get('user_id'))
        email_result = sql_function.get_account(email)
        if int(email_result['user_id']) != user_id:
            error_msg = "Email entered is already in use. Please enter another email address."
        else:
            sql_function.update_customer_details(first_name, last_name, birth_date, title, phone_number, region, city, street_name, email, user_id)
            msg = "Update successful"
    # take latest details_list
    details_list = sql_function.get_customer_details(user_id)
    details_list['birth_date'] = details_list['birth_date'].strftime('%d %b %Y')
    return render_template('customer/update_personal_information.html', details_list=details_list, title_list=sql_function.title_list,
                           region_list=sql_function.region_list, city_list=sql_function.city_list, msg=msg, error_msg=error_msg)


# route for changing password
@app.route('/customer_change_password', methods=['GET', 'POST'])
def customer_change_password():
    # get user_id from session
    # user_id = session["user_id"]
    user_id = 3
    # create message variables to display in templates
    error_msg = ""
    msg = ""
    # get old password from user
    original_password = sql_function.get_account_by_id(user_id)['password'].encode('utf-8')
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
    return render_template('customer/change_password.html', msg=msg, error_msg=error_msg)
