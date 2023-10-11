from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import re
from app import app, check_permissions, scheduler, sql_function, bcrypt


@app.route('/admin/manage_staff', methods=['GET', 'POST'])
def manage_staff():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Manage Staff", "url": "#"}]
    page = request.args.get('page')
    search = request.args.get('search')
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 3:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    if not page:
        sql_page = 0
    else:
        page = int(page)
        sql_page = (page - 1) * 15
    if search:
        staff_list, count = sql_function.search_staff(search, sql_page)
    else:
        staff_list, count = sql_function.get_all_staff(sql_page)
    if request.method == 'POST':
        first_name = request.form.get('first_name').capitalize(),
        last_name = request.form.get('last_name').capitalize(),
        password = request.form.get('password'),
        title = request.form.get('title'),
        email = request.form.get('email'),
        phone_number = request.form.get('phone_number'),
        user_id = request.form.get('user_id')
        if user_id:
            last_msg = "Updated successfully"
            sql_function.update_staff_details(first_name, last_name, title, phone_number, email, user_id)
        else:
            last_msg = "Added successfully"
            sql_function.add_staff(first_name, last_name, title, phone_number, email, password)
    return render_template('admin/manage_staff.html', breadcrumbs=breadcrumbs, staff_list=staff_list, title_list=sql_function.title_list, count=count, staff_search=search, msg=last_msg, error_msg=last_error_msg)


@app.route('/admin/manage_customer', methods=['GET', 'POST'])
def manage_customer():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Manage Customer", "url": "#"}]
    page = request.args.get('page')
    search = request.args.get('search')
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 3:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    if not page:
        sql_page = 0
    else:
        page = int(page)
        sql_page = (page - 1) * 15
    if search:
        customer_list, count = sql_function.search_customer(search, sql_page)
    else:
        customer_list, count = sql_function.get_all_customer(sql_page)
    if request.method == 'POST':
        first_name = request.form.get('first_name').capitalize(),
        last_name = request.form.get('last_name').capitalize(),
        password = request.form.get('password'),
        title = request.form.get('title'),
        email = request.form.get('email'),
        phone_number = request.form.get('phone_number'),
        birth_date = request.form.get('birth_date'),
        region = request.form.get('region'),
        city = request.form.get('city'),
        street_name = request.form.get('street_name'),
        user_id = request.form.get('user_id')
        if user_id:
            last_msg = "Updated successfully"
            sql_function.update_customer_details(first_name, last_name, birth_date, title, phone_number, region, city, street_name, email, user_id)
        else:
            last_msg = "Added successfully"
            sql_function.add_customer(first_name, last_name, birth_date, title, phone_number, region, city, street_name, email, password)
    return render_template('admin/manage_customer.html', breadcrumbs=breadcrumbs, customer_list=customer_list, title_list=sql_function.title_list,
                           city_list=sql_function.city_list, region_list=sql_function.region_list, count=count, customer_search=search, msg=last_msg, error_msg=last_error_msg)


@app.route('/admin/delete_user', methods=['GET', 'POST'])
def delete_user():
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 3:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        previous_url = str(request.referrer)
        urlList = [x for x in previous_url.split('/') if x != '']
        if "manage_staff" in urlList[-1]:
            sql_function.delete_staff(user_id)
            return redirect(previous_url)
        elif "manage_customer" in urlList[-1]:
            sql_function.delete_customer(user_id)
            return redirect(previous_url)
    else:
        session['error_msg'] = "Sorry, we can't find the page you're looking for!."
        return redirect(url_for('dashboard'))
