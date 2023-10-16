from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta, time
from app import app, check_permissions, scheduler, sql_function, upload_image


# route for check out list
@app.route('/staff/check_out_list', methods=['GET', 'POST'])
def check_out_list():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Check Out", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # if method is POST ...
    if request.method == 'POST':
        # get the date from the website
        the_date = datetime.strptime(request.form['the_date'], "%d %b %Y")
        # previous day function
        if 'previous_day' in request.form:
            the_date = the_date - timedelta(days=1)
        # next day function
        elif 'next_day' in request.form:
            the_date = the_date + timedelta(days=1)
        # check out an equipment
        else:
            instance_id = request.form['instance_id']
            equipment_rental_status_id = request.form['equipment_rental_status_id']
            current_datetime = datetime.now().replace(microsecond=0)
            # update an equipment's rental status AND insert a log about the equipment into the log
            sql_function.check_out_equipment(equipment_rental_status_id, instance_id, session['user_id'], current_datetime)
            last_msg = "Equipment checked out successful"
    # otherwise, set the date as today's date
    else:
        the_date = date.today()
    # get every equipment waiting for pickup
    pickup_list = sql_function.get_pickup_equipment(the_date)
    # convert timedelta object to a time object
    for pickup in pickup_list:
        hours = pickup['rental_start_datetime'].seconds // 3600
        minutes = (pickup['rental_start_datetime'].seconds % 3600) // 60
        pickup['rental_start_datetime'] = time(hour=hours, minute=minutes).strftime('%H:%M')
    # convert the date to a user-friendly format
    the_date = the_date.strftime("%d %b %Y")
    return render_template('staff/check_out_list.html', pickup_list=pickup_list, the_date=the_date, breadcrumbs=breadcrumbs, msg=last_msg,
                           error_msg=last_error_msg)

# route for return list
@app.route('/staff/return_list', methods=['GET', 'POST'])
def return_list():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Return List", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # if method is POST ...
    if request.method == 'POST':
        # get the date from the website
        the_date = datetime.strptime(request.form['the_date'], "%d %b %Y")
        # previous day function
        if 'previous_day' in request.form:
            the_date = the_date - timedelta(days=1)
        # next day function
        elif 'next_day' in request.form:
            the_date = the_date + timedelta(days=1)
        # return an equipment
        else:
            instance_id = request.form['instance_id']
            equipment_rental_status_id = request.form['equipment_rental_status_id']
            current_datetime = datetime.now().replace(microsecond=0)
            # update an equipment's rental status based on the current datetime AND insert a log about the equipment into the log
            sql_function.return_equipment(equipment_rental_status_id, instance_id, session['user_id'], current_datetime)
            last_msg = "Equipment returned successful"
    # otherwise, set the date as today's date
    else:
        the_date = date.today()
    # get every rented out equipment.
    sql_return_list = sql_function.get_return_equipment(the_date)
    # convert timedelta object to a time object
    for return_item in sql_return_list:
        hours = return_item['expected_return_datetime'].seconds // 3600
        minutes = (return_item['expected_return_datetime'].seconds % 3600) // 60
        return_item['expected_return_datetime'] = time(hour=hours, minute=minutes).strftime('%H:%M')
    # convert the date to a user-friendly format
    the_date = the_date.strftime("%d %b %Y")
    return render_template('staff/return_list.html', return_list=sql_return_list, the_date=the_date, breadcrumbs=breadcrumbs, msg=last_msg,
                           error_msg=last_error_msg)


# route for maintenance list
@app.route('/staff/maintenance_list', methods=['GET', 'POST'])
def maintenance_list():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Maintenance List", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # if method is POST, mark the instance as completed
    if request.method == 'POST':
        instance_id = request.form['instance_id']
        sql_function.complete_maintenance(instance_id)
        last_msg = "Maintenance finished"
    # get today's date
    the_date = date.today()
    # get every equipment which is under maintenance
    sql_maintenance_list = sql_function.get_maintenance_equipment(the_date)
    # convert the date to a user-friendly format
    for maintenance in sql_maintenance_list:
        maintenance['start_date'] = maintenance['start_date'].strftime("%d %b %Y")
        maintenance['end_date'] = maintenance['end_date'].strftime("%d %b %Y")
    return render_template('staff/maintenance_list.html', maintenance_list=sql_maintenance_list, breadcrumbs=breadcrumbs, msg=last_msg,
                           error_msg=last_error_msg)


@app.route('/staff/more_detail/<detail_id>', methods=['GET', 'POST'])
def more_detail(detail_id):
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Equipment List", "url": "/staff/equipment_list"}, {"text": "Details", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    equipment = sql_function.get_equipment_by_id(detail_id)
    # for item in equipment:
    #     print(item['equipment_id'])
    return render_template('staff/equipment_detail.html', detail_id=detail_id, breadcrumbs=breadcrumbs, equipment=equipment, msg=last_msg,
                           error_msg=last_error_msg)


@app.route('/staff/update_equipment/<detail_id>', methods=['GET', 'POST'])
def update_equipment(detail_id):
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Equipment List", "url": "/staff/equipment_list"}, {"text": "Update Equipment", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    if request.method == 'POST':
        equipment_id = request.form.get('equipment_id')
        image = request.files['image']
        equipment = request.form.get('ename')
        price = request.form.get('price')
        stock = request.form.get('stock')
        driver_license = request.form.get('license')
        length = request.form.get('length')
        width = request.form.get('width')
        height = request.form.get('height')
        description = request.form.get('description')
        detail = request.form.get('detail')
        capitalize_name = equipment.title()
        if image.filename:
            image_url = upload_image(image)
            sql_function.updating_equipment_image(equipment_id, image_url)
            sql_function.updating_equipment(capitalize_name, price, stock, driver_license, length, width, height, description, detail, equipment_id)
        else:
            if driver_license == 'yes':
                driver_license = 1
            elif driver_license == 'no':
                driver_license = 0
            sql_function.updating_equipment(capitalize_name, price, stock, driver_license, length, width, height, description, detail, equipment_id)
        session['msg'] = 'Updated successfully!'
        return redirect(url_for('more_detail', detail_id=detail_id, equipment=equipment))
    equipment = sql_function.get_equipment_by_id(detail_id)
    return render_template('staff/update_equipment.html', detail_id=detail_id, equipment=equipment, breadcrumbs=breadcrumbs, msg=last_msg,
                           error_msg=last_error_msg)


@app.route('/staff/search_result', methods=['GET', 'POST'])
def search_result():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Equipment List", "url": "/staff/equipment_list"}, {"text": "Result", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    # Retrieve word that has been inputed
    search = request.form.get('equipmentsearch')
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # Check if search is not empty or contains only whitespace
    if search and search.strip():
        # equipmentsearch used for partial matching
        equipmentsearch = f'{search}'
        equipment = sql_function.search_equipment_list(equipmentsearch)
        if not equipment:
            # No results found for the search
            last_error_msg = "No equipment found for your search."
            return render_template('staff/equipment_list.html', breadcrumbs=breadcrumbs, equipment=equipment, msg=last_msg, error_msg=last_error_msg)
        else:
            # Results found, render the equipment list
            return render_template('staff/equipment_list.html', breadcrumbs=breadcrumbs, equipment=equipment, msg=last_msg, error_msg=last_error_msg)
    else:
        # Handle the case where search is empty or contains only whitespace
        session['error_msg'] = 'Search field cannot be left blank.'
        return redirect(url_for('equipment_list'))


@app.route('/staff/customerlist')
def customer_list():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Customers List", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    equipment = sql_function.customer_list()
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    return render_template('staff/customer_list.html', breadcrumbs=breadcrumbs, equipment=equipment, msg=last_msg, error_msg=last_error_msg)


@app.route('/staff/equipment_list')
def equipment_list():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Equipments List", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    equipment = sql_function.equipment_details()
    return render_template('staff/equipment_list.html', breadcrumbs=breadcrumbs, equipment=equipment, msg=last_msg, error_msg=last_error_msg)
