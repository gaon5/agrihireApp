from flask import Flask, url_for, request, redirect, render_template, session, jsonify
from datetime import date, datetime, timedelta
import math
import re
import json
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
        if any(categories['name'] == category for categories in sql_function.get_classify()[2].values()):
            breadcrumbs.append({"text": str(category).replace("-", " "), "url": "/equipments/" + str(category)})
            category_id = next((key for key, value in sql_function.get_classify()[2].items() if value['name'] == category), None)
            if sub:
                if sub in sql_function.get_classify()[2][category_id]['subcategories']:
                    sub_id = next((item['sub_id'] for item in sql_function.get_classify()[1] if item['name'] == sub), None)
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
        sub_list = sql_function.get_classify()[2][category_id]
    else:
        sql_equipments, count = sql_function.get_all_equipment(sql_page)
    if 'loggedIn' in session:
        if check_permissions() == 1:
            wishlist = sql_function.get_wishlist(session['user_id'])
    return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, count=count, wishlist=wishlist,
                           sub_list=sub_list, msg=last_msg, error_msg=last_error_msg)


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
        return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, count=count, wishlist=wishlist,
                               equipment_search=equipment, msg=last_msg, error_msg=last_error_msg)
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
        if any(categories['name'] == category for categories in sql_function.get_classify()[2].values()):
            breadcrumbs.append({"text": str(category).replace("-", " "), "url": "/equipments/" + str(category)})
            category_id = next((key for key, value in sql_function.get_classify()[2].items() if value['name'] == category), None)
            sub_list = sql_function.get_classify()[2][category_id]
            if sub:
                if sub in sql_function.get_classify()[2][category_id]['subcategories']:
                    sub_id = next((item['sub_id'] for item in sql_function.get_classify()[1] if item['name'] == sub), None)
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
    disable_list, count = sql_function.get_equipment_disable_list(detail_id)
    if equipment[0]['sub_id'] != sub_id:
        session['error_msg'] = "Sorry, we can't find the page you're looking for!."
        return redirect(url_for('equipments'))
    if request.method == 'POST':
        select_date = request.form.get('datetimes')
    if 'loggedIn' in session:
        if check_permissions() == 1:
            wishlist = sql_function.get_user_wishlist(session['user_id'], detail_id)
    return render_template('customer/equipment_detail.html', detail_id=detail_id, breadcrumbs=breadcrumbs, equipment=equipment, wishlist=wishlist,
                           sub_list=sub_list, count=count, disable_list=disable_list, msg=last_msg, error_msg=last_error_msg)


@app.route('/user_wishlist', methods=['GET', 'POST'])
def user_wishlist():
    breadcrumbs = [{"text": "Wishlist", "url": "/user_wishlist"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    page = request.args.get('page')
    if not page:
        sql_page = 0
    else:
        page = int(page)
        sql_page = (page - 1) * 12
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('equipments'))
    if check_permissions() == 1:
        sql_equipments, count = sql_function.get_equipment_by_wishlist(session['user_id'], sql_page)
        return render_template('customer/wishlist.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, count=count, msg=last_msg,
                               error_msg=last_error_msg)


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


# @app.route('/bookings')
# def bookings():
#     breadcrumbs = [{"text": "Bookings", "url": "#"}]
#     last_msg = session.get('msg', '')
#     last_error_msg = session.get('error_msg', '')
#     session['msg'] = session['error_msg'] = ''
#     if 'loggedIn' in session:
#         sql_bookings = sql_function.get_bookings(session['user_id'])
#         return render_template('customer/bookings.html', bookings=sql_bookings, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)
#     else:
#         session['error_msg'] = 'You are not logged in, please login first.'
#         return redirect(url_for('index'))


@app.route('/bookings')
def bookings():
    breadcrumbs = [{"text": "Bookings", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' in session:
        sql_bookings = sql_function.get_bookings(session['user_id'])
        for booking in sql_bookings:
            if booking['rental_start_datetime']:
                booking['rental_start_datetime'] = booking['rental_start_datetime'].strftime('%d-%m-%Y %H:%M')
            else:
                booking['rental_start_datetime'] = 'N/A'
            
            if booking['expected_return_datetime']:
                booking['expected_return_datetime'] = booking['expected_return_datetime'].strftime('%d-%m-%Y %H:%M')
            else:
                booking['expected_return_datetime'] = 'N/A'
        return render_template('customer/bookings.html', bookings=sql_bookings, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))

@app.route('/update_booking', methods=['POST'])
def update_booking():
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))
    start_date = request.form.get('start_date')
    cost_per_day = float(request.form.get('price'))
    instance_id = request.form.get('instance_id')
    hire_id = request.form.get('hire_id')
    new_end_date = request.form.get('new_end_date')
    new_end_time = request.form.get('new_end_time')
    # Combine the date and time to form a datetime string
    combined_datetime_str = f"{new_end_date} {new_end_time}"
    # Convert the string end_date and rental_start to datetime objects for comparison
    end_date_obj = datetime.strptime(combined_datetime_str, '%Y-%m-%d %H:%M')
    rental_start_obj = datetime.strptime(start_date, '%d-%m-%Y %H:%M')
    # Check if the difference between end_date and rental_start exceeds one week
    if end_date_obj > rental_start_obj + timedelta(weeks=1):
        session['error_msg'] = 'You can only extend the hire period up to a week from the start date.'
        return redirect(url_for('bookings'))
    # Calculate the additional cost for the extension
    extension_duration = end_date_obj - rental_start_obj
    extension_duration_seconds = (end_date_obj - rental_start_obj).total_seconds()
    extension_days = extension_duration.days
    additional_cost = extension_days * cost_per_day
    # Check if extension duration exceeds 12 hours beyond the complete days
    if extension_duration.seconds > 12 * 3600:
        additional_cost += 0.75 * cost_per_day
    session['end_date_obj'] = end_date_obj.strftime('%Y-%m-%d %H:%M:%S')
    session['instance_id'] = instance_id
    session['hire_id'] = hire_id
    session['extension_duration_seconds'] = extension_duration_seconds
    session['additional_cost'] = additional_cost
    return redirect(url_for('payment_form'))





@app.template_filter('duration_format')
def seconds_to_days_hours_seconds(seconds):
    # Convert seconds to days, hours, and seconds
    days, remainder = divmod(seconds, 86400)  # 86400 seconds in a day
    hours, seconds = divmod(remainder, 3600)  # 3600 seconds in an hour
    return f"{days} Days {hours} Hours"


@app.route('/payment_form', methods=['GET', 'POST'])
def payment_form():
    end_date_str = session.get('end_date_obj')
    if end_date_str:
        # Convert the end_date_str back to a datetime object
        end_date_obj = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
        formatted_end_date = end_date_obj.strftime('%d-%m-%Y %H:%M')
    else:
        formatted_end_date = None
    
    instance_id = session['instance_id']
    hire_id = session['hire_id']
    extension_duration = session['extension_duration_seconds']
    additional_cost = session['additional_cost']
    breadcrumbs = [{"text": "Bookings", "url": "/bookings"}, {"text": "Payment", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    # Assuming you have a function to fetch booking details based on instance_id or hire_id
    booking = sql_function.get_booking(hire_id, instance_id)
    if request.method == 'POST':
        payment_type = request.form.get('payment_type')
        payment_type_id = int(payment_type)
        payment_successful = sql_function.update_payment(hire_id, 1, payment_type_id)
        if payment_successful:
            sql_function.update_booking_end_date(end_date_obj, instance_id)
            session['msg'] = "Booking updated successfully"
        else:
            session['error_msg'] = 'Payment failed. Please try again.'
        session['end_date_obj'] = session['instance_id'] = session['hire_id'] = session['extension_duration_seconds'] = session['additional_cost'] = ''
        return redirect(url_for('bookings'))
    return render_template('customer/payment_form.html', booking=booking, extension_duration=extension_duration, formatted_end_date=formatted_end_date,
                           additional_cost=additional_cost, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)


@app.route('/faq')
def faq():
    return render_template('customer/faq.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    breadcrumbs = [{"text": "Contact Us", "url": "#"}]
    last_msg = session.get('msg', '')  # Retrieve and clear the message in one step
    last_error_msg = session.get('error_msg', '')  # Retrieve and clear the error message in one step
    session['msg'] = session['error_msg'] = ''
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        location = request.form.get('location')
        enquiry_type = request.form.get('enquiry_type')
        enquiry_details = request.form.get('enquiry_details')

        # Insert into database
        if sql_function.insert_enquiry(first_name, last_name, email, phone, location, enquiry_type, enquiry_details):
            last_error_msg = "Your enquiry has been submitted successfully!"
        else:
            session['error_msg'] = "There was an error submitting your enquiry. Please try again."

    return render_template('customer/contact.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)



@app.route('/customer_cart')
def customer_cart():
    breadcrumbs = [{"text": "Cart", "url": "#"}]
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
        # print(equipment['quantity'])
        # print(equipment['max_count'])
        equipment['start_time'] = datetime.strftime(start_time, '%d-%m-%Y %H:%M')
        equipment['end_time'] = datetime.strftime(end_time, '%d-%m-%Y %H:%M')
    return render_template('customer/customer_cart.html', equipment_list=equipment_list, total_amount=total_amount, breadcrumbs=breadcrumbs, msg=last_msg,
                           error_msg=last_error_msg)


@app.route('/add_to_cart', methods=['POST', 'get'])
def add_to_cart():
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    datetimes = request.form.get('datetimes')
    previous_url = str(request.referrer)
    start_str, end_str = datetimes.split(' - ')
    start_time = datetime.strptime(start_str, "%d/%m/%Y %H:%M")
    end_time = datetime.strptime(end_str, "%d/%m/%Y %H:%M")
    equipment_id = request.form.get('equipment_id')
    
    
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))
    try:
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
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    cart_item_id = request.form.get('cart_item_id')
    # print(cart_item_id)
    sql_function.sql_delete_item(cart_item_id)
    session['msg'] = "Delete successfully"
    return redirect(url_for('customer_cart'))


@app.route('/edit_details', methods=['POST', 'GET'])
def edit_details():
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))
    user_id = session['user_id']
    quantity = request.form.get('quantity')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    cart_item_id = request.form.get('cart_item_id')
    start_time = datetime.strptime(start_time, '%d-%m-%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time, '%d-%m-%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
    # print(start_time, end_time, quantity, cart_item_id)
    if not (start_time and end_time and cart_item_id and quantity):
        session['error_msg'] = 'Please select the required date and time and quantity.'
        return redirect(url_for('customer_cart'))
    elif end_time <= start_time:
        session['error_msg'] = 'Return time must be after rental time.'
        return redirect(url_for('customer_cart'))
    else:
        sql_function.edit_equipment_in_cart(user_id, cart_item_id, quantity, start_time, end_time)
        session['msg'] = "Update successfully"
        return redirect(url_for('customer_cart'))


@app.route('/payment', methods=['POST', 'GET'])
def payment():
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))
    user_id = session['user_id']
    selected_ids = request.form.get('selectedCartItemIds')
    selected_quantities = request.form.get('selectedQuantities')
    total_amount_final = request.form.get('totalAmountFinal')
    driver_license = request.form.get('driver_license')

    # 将字符串形式的ids和quantities转换为列表
    print(selected_ids)
    print(selected_quantities)
    print(total_amount_final)
    print(driver_license)
    if selected_ids:
        selected_ids_list = [int(id_) for id_ in selected_ids.split(',') if id_.strip()]
    else:
        selected_ids_list = []
    
    if selected_quantities:
        selected_quantities_list = [int(quantity) for quantity in selected_quantities.split(',') if quantity]
    else:
        selected_quantities_list = []
    
    methods = sql_function.payment_method()
    if selected_ids_list == []:
        session['error_msg'] = 'Please choose the equipment in your cart to place order.'
        return redirect(url_for('customer_cart'))
    else:
        equipment_list = sql_function.check_cart(user_id)
        for each in selected_ids_list:
            booking_equipment_id = sql_function.booking_equipment(each)
            # print(booking_equipment_id)
            # print(equipment_list)
            if booking_equipment_id in equipment_list and not driver_license:
                session['msg'] = "Please provide your driver license"
                session['driver_lisence_equipments_price'] = total_amount_final
                session['driver_lisence_equipments_cart_id'] = selected_ids_list
                session['driver_lisence_equipments_quantities'] = selected_quantities_list
                session['method_list'] = methods
                return redirect(url_for('driver_license'))
            
        for selected_id, selected_quantity in zip(selected_ids_list, selected_quantities_list):
            booking_equipment_id = sql_function.booking_equipment(selected_id)
            max_count = sql_function.max_count(booking_equipment_id)
            # print(max_count)

            if selected_quantity > max_count:
                session['error_msg'] = f'The quantity for equipment ID {selected_id} exceeds the maximum allowed value of {max_count}.'
                return redirect(url_for('customer_cart'))
        return render_template('customer/payment.html', msg=last_msg, error_msg=last_error_msg, price=total_amount_final,
                               selectedItemList=selected_ids_list, selected_quantities_list=selected_quantities_list, methods=methods)


@app.route('/complete_payment', methods=['POST','get'])
def complete_payment():
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))
    
    # 检查请求是否包含POST数据
    if request.method == 'POST':
        # 获取表单数据
        selected_items_json = request.form.get('selectedItemList')  # 这是一个JSON字符串
        selected_items = json.loads(selected_items_json)  # 将JSON字符串转换回Python列表

        price = request.form['price']  # 获取价格
        payment_method = request.form.get('paymentMethod')  # 获取用户选择的支付方式
        # print(selected_items)
        # print(price)
        # print(payment_method)
        selected_quantities_json = request.form.get('selectedQuantitiesList')  # 这是一个JSON字符串
        selected_quantities = json.loads(selected_quantities_json)  # 将JSON字符串转换回Python列表

        # 打印调试信息，或进行其他处理
        # print(selected_quantities)
        user_id = session['user_id']
        hire_id = sql_function.hire_list_update(price, user_id)
        # print(hire_id)
        sql_function.payment_update(hire_id, payment_method)
        for i in range(0, len(selected_items)):
            booking_equipment_id = sql_function.booking_equipment(selected_items[i])
            equipment_quantity = selected_quantities[i]
            instance_ids = sql_function.update_equipment_instance(booking_equipment_id, equipment_quantity)
            for instance_id in instance_ids:
                time_diff = sql_function.update_equipment_rental_status(instance_id, selected_items[i], user_id)
                total_seconds = time_diff.total_seconds()
                # 计算具体的天数、小时数、分钟数
                days, remainder = divmod(total_seconds, 86400)  # 86400 seconds per day
                hours, remainder = divmod(remainder, 3600)  # 3600 seconds per hour
                if 0 < hours <= 4:
                    days = days + 0.75
                elif hours == 0:
                    days = days
                else:
                    days = days + 1
                sql_function.update_hire_item(hire_id, instance_id, equipment_quantity, booking_equipment_id, days)
            sql_function.sql_delete_item(selected_items[i])
        session['msg'] = "Order complete. Please check in your bookings. "
        return redirect(url_for('customer_cart'))
    else:
        # 例如，重定向到首页或错误页面
        return redirect(url_for('customer_cart'))


@app.route('/driver_license', methods=['POST','get'])
def driver_license():
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('index'))
    
    driver_license = request.form.get('driver_license')
    print(driver_license)
    price = session['driver_lisence_equipments_price']
    selectedItemList = session['driver_lisence_equipments_cart_id']
    selected_quantities_list = session['driver_lisence_equipments_quantities']
    methods = session['method_list']
        
    return render_template('customer/driver_license.html', msg=last_msg, error_msg=last_error_msg, price=price, selectedItemList=selectedItemList,
                           selected_quantities_list=selected_quantities_list, methods=methods)
