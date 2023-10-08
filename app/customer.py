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
    sub_list = wishlist = None
    page = request.args.get('page')
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
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
                    session['error_msg'] = "Sorry, we can't find the page you're looking for!."
                    return redirect(url_for('equipments'))
        else:
            session['error_msg'] = "Sorry, we can't find the page you're looking for!."
            return redirect(url_for('equipments'))
    if category_id:
        if sub_id:
            sql_equipments, count = sql_function.get_equipment_by_sub(sub_id, sql_page)
        else:
            sql_equipments, count = sql_function.get_equipment_by_category(category_id, sql_page)
        sub_list = sql_function.category[category_id]
    else:
        sql_equipments, count = sql_function.get_all_equipment(sql_page)
    if 'loggedIn' in session:
        wishlist = sql_function.get_wishlist(session['user_id'])
    return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, category_list=sql_function.category_list,
                           count=count, wishlist=wishlist, sub_list=sub_list, msg=last_msg, error_msg=last_error_msg)


@app.route('/equipments/search_equipment', methods=['GET', 'POST'])
def search_equipment():
    breadcrumbs = [{"text": "Equipments", "url": "/equipments"}, {"text": "Search", "url": ""}]
    equipment = request.args.get('equipment')
    wishlist = None
    page = request.args.get('page')
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if not page:
        sql_page = 0
    else:
        page = int(page)
        sql_page = (page - 1) * 12
    if equipment:
        sql_equipments, count = sql_function.get_equipment_by_search(equipment, sql_page)
        if 'loggedIn' in session:
            wishlist = sql_function.get_wishlist(session['user_id'])
        return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, category_list=sql_function.category_list,
                               count=count, wishlist=wishlist, msg=last_msg, error_msg=last_error_msg)
    else:
        session['error_msg'] = "Sorry, we can't find the page you're looking for!."
        return redirect(url_for('equipments'))


@app.route('/equipments/<category>/<sub>/detail', defaults={'detail_id': None})
@app.route('/equipments/<category>/<sub>/detail/<detail_id>', methods=['GET', 'POST'])
def equipment_detail(category, sub, detail_id):
    breadcrumbs = [{"text": "Equipments", "url": "/equipments"}]
    sub_list = wishlist = None
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if category:
        if any(categories['name'] == category for categories in sql_function.category.values()):
            breadcrumbs.append({"text": str(category).replace("-", " "), "url": "/equipments/" + str(category)})
            category_id = next((key for key, value in sql_function.category.items() if value['name'] == category), None)
            sub_list = sql_function.category[category_id]
            if sub:
                if sub in sql_function.category[category_id]['subcategories']:
                    sub_id = next((item['sub_id'] for item in sql_function.sub_category_list if item['name'] == sub), None)
                    breadcrumbs.append({"text": str(sub).replace("-", " "), "url": "/equipments/" + str(category) + "/" + str(sub)})
                else:
                    session['error_msg'] = "Sorry, we can't find the page you're looking for!."
                    return redirect(url_for('equipments'))
        else:
            session['error_msg'] = "Sorry, we can't find the page you're looking for!."
            return redirect(url_for('equipments'))
    if not detail_id:
        session['error_msg'] = "Sorry, we can't find the page you're looking for!."
        return redirect(url_for('equipments'))
    breadcrumbs.append({"text": "Detail", "url": ""})
    equipment = sql_function.get_equipment_by_id(detail_id)
    if equipment[0]['sub_id'] != sub_id:
        session['error_msg'] = "Sorry, we can't find the page you're looking for!."
        return redirect(url_for('equipments'))
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
    if 'loggedIn' in session:
        wishlist = sql_function.get_user_wishlist(session['user_id'], detail_id)
    return render_template('customer/equipment_detail.html', detail_id=detail_id, breadcrumbs=breadcrumbs, equipment=equipment,
                           category_list=sql_function.category_list, wishlist=wishlist, sub_list=sub_list, msg=last_msg, error_msg=last_error_msg)


@app.route('/user_wishlist', methods=['GET', 'POST'])
def user_wishlist():
    breadcrumbs = [{"text": "Equipments", "url": "/equipments"}, {"text": "Wishlist", "url": "/user_wishlist"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    page = request.args.get('page')
    if not page:
        sql_page = 0
    else:
        page = int(page)
        sql_page = (page - 1) * 12
    if 'loggedIn' in session:
        sql_equipments, count = sql_function.get_equipment_by_wishlist(session['user_id'], sql_page)
        return render_template('customer/wishlist.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, category_list=sql_function.category_list,
                               count=count, msg=last_msg, error_msg=last_error_msg)
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('equipments'))


@app.route('/add_favorite/<int:equipment_id>', methods=['GET', 'POST'])
def add_favorite(equipment_id):
    previous_url = str(request.referrer)
    if 'loggedIn' in session:
        sql_function.add_wishlist(session['user_id'], equipment_id)
        session['msg'] = 'Added successfully'
        return redirect(previous_url)
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(previous_url)


@app.route('/remove_favorite/<int:equipment_id>', methods=['GET', 'POST'])
def remove_favorite(equipment_id):
    previous_url = str(request.referrer)
    if 'loggedIn' in session:
        sql_function.delete_wishlist(session['user_id'], equipment_id)
        session['msg'] = 'Removed successfully'
        return redirect(previous_url)
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(previous_url)


@app.route('/bookings')
def bookings():
    breadcrumbs = [{"text": "Personal Center", "url": "#"}, {"text": "Bookings", "url": "/bookings"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' in session:
        sql_bookings = sql_function.get_bookings(session['user_id'])
        return render_template('customer/bookings.html', bookings=sql_bookings, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))


@app.route('/delete_booking/<int:instance_id>/<int:hire_id>', methods=['POST'])
def delete_booking(instance_id, hire_id):
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' in session:
        sql_function.delete_booking(instance_id, hire_id)
        session['msg'] = "Booking deleted successfully"
        return redirect(url_for('bookings'))
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))


@app.route('/update_booking/<int:instance_id>', methods=['POST'])
def update_booking(instance_id):
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    end_date = request.form.get('end_date')
    if 'loggedIn' in session:
        sql_function.update_booking_end_date(instance_id, end_date)
        session['msg'] = "Booking updated successfully"
        return redirect(url_for('bookings'))
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))



@app.route('/faq')
def faq():
    contact_details = "support@example.com"  # This can also come from a database or configuration.
    return render_template('customer/faq.html', contact=contact_details)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    breadcrumbs = [{"text": "contact", "url": "/contact"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if request.method == 'POST':
        # Get form data (to be stored or processed)
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        location = request.form.get('location')
        enquiry_type = request.form.get('enquiry_type')
        enquiry_details = request.form.get('enquiry_details')

        
        session['msg'] = "'Your enquiry has been submitted successfully!', 'success'"

        return render_template('customer/contact.html', msg=last_msg, error_msg=last_error_msg)


    return render_template('customer/contact.html')
