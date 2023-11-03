from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta, time
from app import app, check_permissions, scheduler, sql_function, upload_image

# route for staff to access the enquiries submitted 
@app.route('/staff/get_enquiries')
def get_enquiries():
    # Check if user is logged in
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))  # Assume there is a login route defined
    # Check if user has required permissions
    if check_permissions() != 2: # Implement check_permissions
        session['error_msg'] = 'You are not authorized to access this page.'
        return redirect(url_for('dashboard'))  # Redirect to a safe page
    # Fetch enquiries from database
    enquiries = sql_function.get_all_enquiries()
    # Display enquiries
    return render_template('staff/enquiries.html', enquiries=enquiries)

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

# route for displaying further details of an equipment
@app.route('/staff/more_detail', methods=['GET', 'POST'])
def more_detail():
    detail_id = request.args['detail_id']
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
    # get details of an equipment
    equipment = sql_function.get_more_detail(detail_id)
    return render_template('staff/equipment_detail.html', detail_id=detail_id, breadcrumbs=breadcrumbs, equipment=equipment, msg=last_msg,
                           error_msg=last_error_msg)

# route for updating equipment based on the id
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
    # get equipment and images
    equipment = sql_function.get_equipment_by_id_(detail_id)
    image_priority = sql_function.image_priority(detail_id)
    img = sql_function.get_more_detail(detail_id)
    main, sub, x, x = sql_function.get_classify()
    # if the user submits anything, get the submitted form 
    if request.method == 'POST':
        equipment_id = request.form.get('equipment_id')
        image_ids = request.form.getlist('image_id')
        main_image = request.files['mainimage']
        image = request.files['image']
        sub_category = request.form.get('sub_category')
        equipment = request.form.get('ename')
        price = request.form.get('price')
        stock = request.form.get('stock')
        threshold = request.form.get('min')
        driver_license = request.form.get('license')
        length = request.form.get('length')
        width = request.form.get('width')
        height = request.form.get('height')
        description = request.form.get('description')
        detail = request.form.get('detail')
        capitalize_name = equipment.title()
        main_image_exist = sql_function.check_existing_main_image(equipment_id)
        images = []
        # upload images
        if main_image.filename:
            images.append([upload_image(main_image), 1])
        if image.filename:
            images.append([upload_image(image), 0])
        # validate driver license
        if driver_license == 'yes':
            driver_license = 1
        elif driver_license == 'no':
            driver_license = 0
        else:
            raise ValueError("Invalid value for driver's license")
        # update information of the equipment based on the inputs
        sql_function.updating_equipment(capitalize_name, price, stock, length, width, height, driver_license, threshold, description, detail, equipment_id,
                                        images,image_ids,sub_category)
        session['msg'] = 'Updated successfully!'
        return redirect(url_for('more_detail', detail_id = detail_id))
    return render_template('staff/update_equipment.html',detail_id=detail_id, img=img, main=main, sub=sub, equipment=equipment,
                           image_priority=image_priority, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)

# route for adding an equipment
@app.route('/staff/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Equipment List", "url": "/staff/equipment_list"}, {"text": "Add Equipment", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # get main category and sub category
    main, sub, x, x = sql_function.get_classify()
    # if the method is post, get the form submitted by the user
    if request.method == 'POST':
        main_image = request.files['mainimage']
        image = request.files['image']
        sub_category = request.form.get('sub_category')
        equipment = request.form.get('ename')
        price = request.form.get('price')
        stock = request.form.get('stock')
        threshold = request.form.get('min')
        driver_license = request.form.get('license')
        length = request.form.get('length')
        width = request.form.get('width')
        height = request.form.get('height')
        description = request.form.get('description')
        detail = request.form.get('detail')
        capitalize_name = equipment.title()
        images = []
        # upload images
        if main_image.filename:
            images.append([upload_image(main_image), 1])
        if image.filename:
            images.append([upload_image(image), 0])
        # validate driver license
        if driver_license == 'yes':
            driver_license = 1
        elif driver_license == 'no':
            driver_license = 0
        else:
            raise ValueError("Invalid value for driver's license")
        # create a new equipment based on the user inputs
        sql_function.add_equipment(capitalize_name, price, stock, length, width, height, driver_license, threshold, description, detail, images, sub_category)
        session['msg'] = 'Equipment has been added!'
        return redirect(url_for('add_equipment', equipment=equipment))
    return render_template('staff/add_equipment.html', main=main, sub=sub, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)

# route for deleting an equipment
@app.route('/staff/delete_equipment', methods=['GET','POST'])
def delete_equipment():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Equipment List", "url": "/staff/equipment_list"}, {"text": "Delete Equipment", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    equipment_id = request.form.get('equipment_id')
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # get equipment based on equipment id, and delete the equipment from the database
    equipment = sql_function.get_equipment_by_id_(equipment_id)
    sql_function.deleting_equipment(equipment_id)
    session['msg'] = "Deleted successfully"
    return redirect(url_for('equipment_list', equipment=equipment, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg))

# route for searching an equipment
@app.route('/staff/search_result', methods=['GET', 'POST'])
def search_result():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Equipment List", "url": "/staff/equipment_list"}, {"text": "Result", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    # Retrieve word that has been inputted
    search = request.form.get('equipment_search')
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # Check if search is not empty or contains only whitespace
    if search and search.strip():
        # equipment_search used for partial matching
        equipment_search = f'{search}'
        equipment = sql_function.search_equipment_list(equipment_search)
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

# route to get a list of customers
@app.route('/staff/customer_list', methods=['GET', 'POST'])
def customer_list():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Customers List", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # if the method is post, return the customers which match the search
    if request.method == 'POST':
        search = request.form.get('search')
        customers, count = sql_function.search_customer(search, 0)
    else:
        # get every customer in the database
        customers, count = sql_function.search_customer('', 0)
    # reformat the birth date 
    for customer in customers:
        customer['birth_date'] = customer['birth_date'].strftime('%d %b %Y')
    return render_template('staff/customer_list.html', breadcrumbs=breadcrumbs, customers=customers, msg=last_msg, error_msg=last_error_msg)

# route to access customer details 
@app.route('/staff/customer_details', methods=['GET', 'POST'])
def customer_details():
    customer_id = request.args['customer_id']
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Customer List", "url": "/staff/customer_list"}, {"text": "Details", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 2:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    customers, count = sql_function.search_customer('', 0)
    # Get the selected customer
    for customer in customers:
        if str(customer['customer_id']) == customer_id:
            aCustomer = customer
            user_id = customer['user_id']
    # format the date
    aCustomer['birth_date'] = aCustomer['birth_date'].strftime('%d %b %Y')
    # get every booking made by the customers
    bookings = sql_function.get_bookings(user_id)
    for booking in bookings:
        booking['rental_start_datetime'] = booking['rental_start_datetime'].strftime('%d %b %Y')
        booking['expected_return_datetime'] = booking['expected_return_datetime'].strftime('%d %b %Y')
    return render_template('staff/customer_details.html', customer_id=customer_id, aCustomer=aCustomer, breadcrumbs=breadcrumbs,
                            customer=customer, bookings=bookings,
                            msg=last_msg, error_msg=last_error_msg)

# route for accessing a list of equipments
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
    # get a list of equipments
    equipment = sql_function.equipment_details()
    return render_template('staff/equipment_list.html', breadcrumbs=breadcrumbs, equipment=equipment, msg=last_msg, error_msg=last_error_msg)

# route for setting status for an instance of an equipment
@app.route('/staff/set_instance', methods = ["POST", "GET"])
def set_instance():
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
    # get every equipment instance
    equipment = sql_function.equipment_instance()
    for i in equipment:
        item=i
    # get every equipment
    all = sql_function.all_equipment()
    # get every instance's status
    i_status = sql_function.instance_status()
    # if the method is post, get user inputs
    if request.method == 'POST':
        equipment_id = request.form.get('equipment_id')
        chosen_status = request.form.get('instance')
        current_status = request.form.get('instance_status')
        if current_status and current_status != 'None':
            instance_id = int(current_status.split()[0])
            current_id = int(current_status.split()[1])   
        else:
            # Handle the case where current_status is 'None' or None
            # You can set appropriate default values or handle it as needed.
            instance_id = None  # Set to a suitable default value or handle the case.
            current_id = None
        # update status of the equipment
        sql_function.change_status(chosen_status, instance_id, equipment_id)
        session['msg'] = 'Status has changed successfully!'
        return redirect(url_for('set_instance'))    
    return render_template('staff/equipment_instance.html',breadcrumbs=breadcrumbs,item=item, i_status=i_status, all=all, equipment=equipment, msg=last_msg, error_msg=last_error_msg)
