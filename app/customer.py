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
    return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, category_list=sql_function.category_list, count=count)


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



@app.route('/bookings')
def bookings():
    msg = request.args.get('msg')
    try:
        user_id = session.get('user_id')  # Assuming user_id is stored in the session
        #print(user_id)
        if user_id is None:
            # Redirect to login page if user_id is not available in the session
            return redirect(url_for('login'))
        
        # Get customer_id using user_id
        customer_id = sql_function.get_customer_id_by_user_id(user_id)
        if customer_id is None:
            # Handle the case where there is no corresponding customer_id for the user_id
            return "No corresponding customer for the logged-in user", 400
        
        # Get bookings using customer_id
        data = sql_function.get_bookings_by_customer_id(customer_id)
        #print(data)
        
        # Render the template with the fetched bookings
        return render_template('customer/bookings.html', bookings=data, msg=msg)
    
    except Exception as e:
        # Handle any other exceptions that might occur
        return f"An error occurred: {str(e)}", 500




@app.route('/delete_booking/<int:instance_id>', methods=['POST'])
def delete_booking(instance_id):
    try:
        user_id = session.get('user_id')  # Assuming user_id is stored in the session
        if user_id is None:
            # Redirect to login page if user_id is not available in the session
            return redirect(url_for('login'))
        
        sql_function.delete_booking_by_instance_id(instance_id)
        msg = "Booking updated successfully"
        
        return redirect(url_for('bookings', msg=msg))
        
    
    except Exception as e:
       
        
        # Handle any other exceptions that might occur
        return f"An error occurred: {str(e)}", 500






@app.route('/update_booking/<int:instance_id>', methods=['POST'])
def update_booking(instance_id):
    try:
        user_id = session.get('user_id')  # Assuming user_id is stored in the session
        if user_id is None:
            # Redirect to login page if user_id is not available in the session
            return redirect(url_for('login'))

        # Fetch the new end date from form data
        new_end_date = request.form.get('new_end_date')
        if not new_end_date:
            return "Invalid data: Missing end date", 400
        #print(new_end_date)
        #print(type(new_end_date))
        
        sql_function.update_booking_end_date(instance_id, new_end_date)
        msg = "Booking updated successfully"
        
        return redirect(url_for('bookings', msg=msg))

    except Exception as e:
        return f"An error occurred: {str(e)}", 500



@app.route('/some_route')
def some_route():
    user_id = session.get('user_id')
    if user_id:
        print(user_id)
        return str(user_id)  # just for demo, return it as a response
    else:
        return 'User_id not in session'