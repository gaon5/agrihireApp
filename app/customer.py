from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import re
from app import app, check_permissions, sql_function


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
        if check_permissions() == 1:
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
            if check_permissions() == 1:
                wishlist = sql_function.get_wishlist(session['user_id'])
        return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, category_list=sql_function.category_list,
                               count=count, wishlist=wishlist, equipment_search=equipment, msg=last_msg, error_msg=last_error_msg)
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
        if check_permissions() == 1:
            wishlist = sql_function.get_user_wishlist(session['user_id'], detail_id)
    return render_template('customer/equipment_detail.html', detail_id=detail_id, breadcrumbs=breadcrumbs, equipment=equipment,
                           category_list=sql_function.category_list, wishlist=wishlist, sub_list=sub_list, msg=last_msg, error_msg=last_error_msg)


@app.route('/user_wishlist', methods=['GET', 'POST'])
def user_wishlist():
    breadcrumbs = [{"text": "Personal Center", "url": "#"}, {"text": "Wishlist", "url": "/user_wishlist"}]
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
        if check_permissions() == 1:
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
    breadcrumbs = [{"text": "Personal Center", "url": "#"}, {"text": "Bookings", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' in session:
        sql_bookings = sql_function.get_bookings(session['user_id'])
        return render_template('customer/bookings.html', bookings=sql_bookings, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))


@app.route('/delete_booking', methods=['POST'])
def delete_booking():
    session['msg'] = session['error_msg'] = ''
    instance_id = request.form.get('instance_id')
    hire_id = request.form.get('hire_id')
    if 'loggedIn' in session:
        sql_function.sql_delete_booking(instance_id, hire_id)
        session['msg'] = "Booking deleted successfully"
        return redirect(url_for('bookings'))
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))


@app.route('/update_booking', methods=['POST'])
def update_booking():
    session['msg'] = session['error_msg'] = ''
    end_date = request.form.get('end_date')
    instance_id = request.form.get('instance_id')
    if 'loggedIn' in session:
        sql_function.update_booking_end_date(instance_id, end_date)
        session['msg'] = "Booking updated successfully"
        return redirect(url_for('bookings'))
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))


@app.route('/faq')
def faq():
    return render_template('customer/faq.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    breadcrumbs = [{"text": "Contact Us", "url": "#"}]
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
# send to database
        last_msg = "'Your enquiry has been submitted successfully!'"
    return render_template('customer/contact.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)


@app.route('/customer_cart')
def customer_cart():
    breadcrumbs = [{"text": "Personal Center", "url": "#"}, {"text": "Cart", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))
    user_id = session['user_id']
    equipment_list = sql_function.my_cart(user_id)
    total_amount = 0
    for equipment in equipment_list:
        start_time = equipment['start_time']
        end_time = equipment['end_time']
        # 计算时间差
        time_diff = end_time - start_time

        # 获取时间差的总秒数
        total_seconds = time_diff.total_seconds()

        # 计算具体的天数、小时数、分钟数
        days, remainder = divmod(total_seconds, 86400)  # 86400 seconds per day
        hours, remainder = divmod(remainder, 3600)  # 3600 seconds per hour
        minutes, _ = divmod(remainder, 60)
        if 0 < hours <= 4:
            days = days + 0.75
        elif hours == 0:
            days = days
        else:
            days = days + 1
        unit_price = float(equipment['price'])
        total_item_price = unit_price * days
        equipment['price'] = total_item_price
        total_amount = total_amount + total_item_price
        # print(type(equipment['price']))
        # print(f"{days} days, {hours} hours, {minutes} minutes")
        max_amount = sql_function.max_count(equipment['equipment_id'])
        equipment['count'] = max_amount

    return render_template('customer/customer_cart.html', equipment_list=equipment_list, total_amount=total_amount, breadcrumbs=breadcrumbs, msg=last_msg,
                           error_msg=last_error_msg)


@app.route('/add_to_cart', methods=['POST', 'get'])
def add_to_cart():
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    equipment_id = request.form.get('equipment_id')
    session['msg'] = session['error_msg'] = ''
    previous_url = str(request.referrer)
    if not (start_time and end_time and equipment_id):
        session['error_msg'] = 'Please select the required date and time.'
        return redirect(previous_url)
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))
    try:
        start_time = datetime.strptime(start_time, '%d-%m-%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time, '%d-%m-%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
        # print(start_time, end_time)
        if start_time >= end_time:
            session['error_msg'] = 'Start time must be before end time.'
            return redirect(previous_url)
        else:
            sql_function.add_equipment_into_cart(session['user_id'], equipment_id, 1, start_time, end_time)
            session['msg'] = "Add to cart successfully"
            return redirect(previous_url)
    except ValueError:
        session['error_msg'] = 'Invalid date or time format. Please use DD-MM-YYYY HH:MM.'
        return redirect(previous_url)


@app.route('/delete_item', methods=['POST'])
def delete_item():
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))
    session['msg'] = session['error_msg'] = ''
    cart_item_id = request.form.get('cart_item_id')
    sql_function.sql_delete_item(cart_item_id)
    session['msg'] = "Delete successfully"
    return redirect(url_for('customer_cart'))


@app.route('/edit_details', methods=['POST', 'GET'])
def edit_details():
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))
    user_id = session['user_id']
    print(user_id)
    data = request.get_json()
    print(data)
    # 从数据中提取特定的值
    cart_item_id = data.get('cart_item_id')
    quantity = data.get('quantity')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    print(start_time)
    if not (start_time and end_time and cart_item_id and quantity):
        session['error_msg'] = 'Please select the required date and time and quantity.'
    else:
        sql_function.edit_equipment_in_cart(user_id, cart_item_id, quantity, start_time, end_time)
        session['msg'] = "Update successfully"
        return redirect(url_for('customer_cart'))


@app.route('/payment', methods=['POST'])
def payment():
    pass
