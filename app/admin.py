from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
from app import app, check_permissions, scheduler, sql_function
import calendar


# route for managing categories
@app.route('/admin/manage_category', methods=['GET', 'POST'])
def manage_category():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Manage Category", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 3:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # if method is POST ...
    if request.method == 'POST':
        # if add button is pressed, insert a new category
        if 'add' in request.form:
            new_category = request.form['new_category']
            # check the input name is not repeated
            flag = sql_function.validate_category(new_category)
            if flag:
                last_error_msg = 'Cannot add this category. Please make sure the category is different from the others'
            else:
                sql_function.insert_category(new_category)
                last_msg = "New category added"
        # if the edit button is pressed, update the name of the category
        elif 'edit' in request.form:
            category_name = request.form['category_name']
            category_id = request.form['category_id']
            # check the input name is not repeated
            flag = sql_function.validate_category(category_name)
            if flag:
                last_error_msg = 'Cannot update this category. Please make sure the category is different from the others'
            else:
                sql_function.edit_category(category_id, category_name)
                last_msg = "Category edited"
        # otherwise, the delete button is pressed and delete the selected category
        else:
            category_id = request.form['category_id']
            # check if the category is linked to any sub-category
            flag = sql_function.check_category(category_id)
            # if there is connection, display an error message
            if flag:
                last_error_msg = 'Cannot delete this category. Please make sure the category is not linked to any sub-category'
            # otherwise, delete the category
            else:
                sql_function.delete_category(category_id)
                last_msg = "Category deleted"
    # get every category from the database
    return render_template('admin/manage_category.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)


# route for managing categories
@app.route('/admin/manage_subcategory', methods=['GET', 'POST'])
def manage_subcategory():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Manage Sub Category", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 3:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # if method is POST ...
    if request.method == 'POST':
        # if add button is pressed, insert a new category
        if 'add' in request.form:
            main_category_id = request.form['main_category_id']
            new_sub_category = request.form['new_sub_category']
            # Check the sub category name is not repeated
            flag = sql_function.validate_subcategory(new_sub_category, main_category_id)
            if flag:
                last_error_msg = 'Cannot add this sub category. Please make sure the sub category is different from the others'
            else:
                sql_function.insert_subcategory(main_category_id, new_sub_category)
                last_msg = "New sub category added"
        # if the change button is pressed, change the main category of the sub category
        elif 'change' in request.form:
            sub_category_id = request.form['sub_category_id']
            main_category_id = request.form['main_category_id_2']
            sql_function.change_category(sub_category_id, main_category_id)
            last_msg = "Main category for the sub category updated"
        # if the edit button is pressed, update the name of the category
        elif 'edit' in request.form:
            subcategory_name = request.form['subcategory_name']
            subcategory_id = request.form['subcategory_id']
            category_id = request.form['category_id']
            # Check the sub category name is not repeated
            flag = sql_function.validate_subcategory(subcategory_name, category_id)
            if flag:
                last_error_msg = 'Cannot update this sub category. Please make sure the sub category is different from the others'
            else:
                sql_function.edit_subcategory(subcategory_id, subcategory_name)
                last_msg = "Sub category edited"
        # otherwise, the delete button is pressed and delete the selected category
        else:
            subcategory_id = request.form['subcategory_id']
            # check if the sub category is link to any equipment
            flag = sql_function.check_subcategory(subcategory_id)
            # if there is connection, display an error message
            if flag:
                last_error_msg = 'Cannot delete this sub category. Please make sure the sub category is not linked to any equipment first.'
            # otherwise, delete the category
            else:
                sql_function.delete_subcategory(subcategory_id)
                last_msg = "Sub category deleted"
    return render_template('admin/manage_subcategory.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)


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
    if request.method == 'POST':
        first_name = request.form.get('first_name').capitalize()
        last_name = request.form.get('last_name').capitalize()
        password = request.form.get('password')
        title = request.form.get('title')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        user_id = request.form.get('user_id')
        user_detail = sql_function.get_account(email)
        if user_id:
            if user_detail:
                if int(user_id) != user_detail['user_id']:
                    session['error_msg'] = 'Email already exists!'
                    return redirect(str(request.referrer))
            last_msg = "Updated successfully"
            sql_function.update_staff_details(first_name, last_name, title, phone_number, email, user_id)
        else:
            last_msg = "Added successfully"
            sql_function.add_staff(first_name, last_name, title, phone_number, email, password)
    if search:
        staff_list, count = sql_function.search_staff(search, sql_page)
    else:
        staff_list, count = sql_function.get_all_staff(sql_page)
    return render_template('admin/manage_staff.html', breadcrumbs=breadcrumbs, staff_list=staff_list, title_list=sql_function.title_list, count=count,
                           staff_search=search, msg=last_msg, error_msg=last_error_msg)


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
    if request.method == 'POST':
        first_name = request.form.get('first_name').capitalize()
        last_name = request.form.get('last_name').capitalize()
        password = request.form.get('password')
        title = request.form.get('title')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        birth_date = datetime.strptime(request.form.get('birth_date'), '%d %b %Y').strftime('%Y-%m-%d')
        region = request.form.get('region')
        city = request.form.get('city')
        street_name = request.form.get('street_name')
        user_id = request.form.get('user_id')
        user_detail = sql_function.get_account(email)
        if user_id:
            if user_detail:
                if int(user_id) != user_detail['user_id']:
                    session['error_msg'] = 'Email already exists!'
                    return redirect(str(request.referrer))
            last_msg = "Updated successfully"
            sql_function.update_customer_details(first_name, last_name, birth_date, title, phone_number, region, city, street_name, email, user_id)
        else:
            last_msg = "Added successfully"
            sql_function.add_customer(first_name, last_name, birth_date, title, phone_number, region, city, street_name, email, password)
    if search:
        customer_list, count = sql_function.search_customer(search, sql_page)
    else:
        customer_list, count = sql_function.get_all_customer(sql_page)
    return render_template('admin/manage_customer.html', breadcrumbs=breadcrumbs, customer_list=customer_list, title_list=sql_function.title_list,
                           city_list=sql_function.city_list, region_list=sql_function.region_list, count=count, customer_search=search, msg=last_msg,
                           error_msg=last_error_msg)


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


@app.route('/admin/password', methods=['GET', 'POST'])
def admin_password():
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 3:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('set_password')
        sql_function.set_password(password, user_id)
        previous_url = str(request.referrer)
        return redirect(previous_url)
    else:
        session['error_msg'] = "Sorry, we can't find the page you're looking for!."
        return redirect(url_for('dashboard'))


# App route for financial report
@app.route('/admin/financial_report', methods=['GET', 'POST'])
def financial_report():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Financial Report", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 3:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # default variables
    title = ''
    year_list = []
    for i in range(2020, 2025):
        year_list.append(i)
    month_list = []
    for month in range(1, 13):
        month_list.append(calendar.month_name[month])
    details_list = []
    revenue_list = []
    category_list = []
    category_total = []
    method_list = []
    method_total = []
    financial_months = []
    income_list = []
    total_revenue = 0
    month_flag = False
    year_flag = False
    # if the user choose a report type
    if request.form.get('report_type'):
        report_type = request.form.get('report_type')
        if report_type == 'month':
            month_flag = True
        else:
            year_flag = True
    # if the user chooses monthly report
    elif request.form.get('month_year'):
        # convert month name into number
        month_number = '{:02d}'.format(month_list.index(request.form.get('month')) + 1)
        # combine year and month into a date string
        start_date = request.form.get('month_year') + '-' + month_number + '-01'
        # get every payment details in a certain month
        details_list = sql_function.get_monthly_details(start_date)
        revenue_list = sql_function.get_monthly_payment(start_date)
        title = 'Monthly Report on {} {}'.format(request.form.get('month'), request.form.get('month_year'))
    # if the user chooses annual report
    elif request.form.get('year'):
        # get the ending date of the financial year
        financial_date = request.form.get('year') + '-03-31'
        # get every payment details in a financial year
        details_list = sql_function.get_annual_details(financial_date)
        revenue_list = sql_function.get_annual_payment(financial_date)
        title = 'Annual Report between 1st April {} and 31st March {}'.format(int(request.form.get('year')) - 1, request.form.get('year'))
        financial_months = ['04', '05', '06', '07', '08', '09', '10', '11', '12', '01', '02', '03']
        # get payment details for each month
        for i in range(1, 13):
            income_list.append(0)
        for i in range(0, len(financial_months), 1):
            for revenue in revenue_list:
                if revenue['payment_datetime'].date().strftime('%Y-%m-%d')[5:7] == financial_months[i]:
                    income_list[i] += revenue['price']
        # Reconstruct month_list
        financial_months = []
        for i in range(4, 13, 1):
            string = calendar.month_name[i] + ' ' + str(int(request.form.get('year')) - 1)
            financial_months.append(string)
        for i in range(1, 4, 1):
            string = calendar.month_name[i] + ' ' + request.form.get('year')
            financial_months.append(string)
    # build up category list
    for detail in details_list:
        if detail['category_name'] not in category_list:
            category_list.append(detail['category_name'])
            category_total.append(0)
    # build up every category total payment
    for detail in details_list:
        for i in range(0, len(category_list), 1):
            if category_list[i] == detail['category_name']:
                category_total[i] += detail['price']
    # build up method list
    for revenue in revenue_list:
        if revenue['payment_type'] not in method_list:
            method_list.append(revenue['payment_type'])
            method_total.append(0)
    # build up every method total payment
    for revenue in revenue_list:
        for i in range(0, len(method_list), 1):
            if method_list[i] == revenue['payment_type']:
                method_total[i] += revenue['price']
    # get the total revenue of the month
    for revenue in revenue_list:
        total_revenue += revenue['price']
    return render_template('admin/financial_report.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg, month_flag=month_flag,
                           year_flag=year_flag, month_list=month_list, year_list=year_list, category_list=category_list, category_total=category_total,
                           method_list=method_list, method_total=method_total, total_revenue=total_revenue, financial_months=financial_months,
                           income_list=income_list, title=title)


# App route for maintenance report
@app.route('/admin/maintenance_report', methods=['GET', 'POST'])
def maintenance_report():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Maintenance Report", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 3:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # default variables
    title = ''
    details_list = []
    year_list = []
    for i in range(2020,2025):
        year_list.append(i)
    month_list = []
    for month in range(1, 13):
        month_list.append(calendar.month_name[month])
    month_flag = False
    year_flag = False
    category_list = []
    category_total_number = []
    category_total_cost = []
    total_number = 0
    total_cost = 0
    number_list = [] 
    cost_list = []
    months = []
    # if the user choose a report type
    if request.form.get('report_type'):
        report_type = request.form.get('report_type')
        if report_type == 'month':
            month_flag = True
        else:
            year_flag = True
    # if the user chooses monthly report
    elif request.form.get('month_year'):
        # convert month name into number
        month_number = '{:02d}'.format(month_list.index(request.form.get('month')) + 1)
        # combine year and month into a date string
        start_date = request.form.get('month_year') + '-' + month_number + '-01'
        # get every maintenance details in a certain month
        details_list = sql_function.get_monthly_maintenances(start_date)
        title = 'Monthly Report on {} {}'.format(request.form.get('month'), request.form.get('month_year'))
    # if the user chooses annual report
    elif request.form.get('year'):
        # get the ending date of the financial year
        start_date = request.form.get('year') + '-01-01'
        # get every maintenance details in a year
        details_list = sql_function.get_annual_maintenances(start_date)
        title = 'Annual Report between 1st January {} and 31st December {}'.format(request.form.get('year'), request.form.get('year'))
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        # get number of maintenance and maintenance costs for each month
        for i in range(1, 13):
            number_list.append(0)
            cost_list.append(0)
        for i in range(0, len(month_list), 1):
            for detail in details_list:
                if detail['maintenance_start_date'].strftime('%Y-%m-%d')[5:7] == months[i]:
                    number_list[i] += 1
                    cost_list[i] += detail['maintenance_cost']
        # Reconstruct month_list
        months = []
        for i in range(1, 13, 1):
            string = calendar.month_name[i] + ' ' + request.form.get('year')
            months.append(string)
    # build up the category list
    for detail in details_list:
        if detail['category_name'] not in category_list:
            category_list.append(detail['category_name'])
            category_total_number.append(0)
            category_total_cost.append(0)
    # get number of maintenance and maintenance cost for each category
    for i in range(0, len(category_list), 1):
        for detail in details_list:
            if detail['category_name'] == category_list[i]:
                category_total_number[i] += 1
                category_total_cost[i] += detail['maintenance_cost']
                total_number += 1
                total_cost += detail['maintenance_cost']
    return render_template('admin/maintenance_report.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg, month_flag=month_flag,
                           year_flag=year_flag, month_list=month_list, year_list=year_list, category_list=category_list,
                           category_total_number=category_total_number, category_total_cost=category_total_cost, total_number=total_number,
                           total_cost=total_cost, number_list=number_list, cost_list=cost_list, months=months, title=title)


# App route for maintenance report
@app.route('/admin/equipment_report', methods=['GET', 'POST'])
def equipment_report():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Equipment Report", "url": "#"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    if check_permissions() != 3:
        session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
        return redirect(url_for('index'))
    # default variables
    title = ''
    details_list = []
    year_list = []
    for i in range(2020,2025):
        year_list.append(i)
    month_list = []
    for month in range(1, 13):
        month_list.append(calendar.month_name[month])
    month_flag = False
    year_flag = False
    category_list = []
    category_total_number = []
    category_total_hour = []
    total_number = 0
    total_hour = 0
    number_list = [] 
    hour_list = []
    months = []
    # if the user choose a report type
    if request.form.get('report_type'):
        report_type = request.form.get('report_type')
        if report_type == 'month':
            month_flag = True
        else:
            year_flag = True
    # if the user chooses monthly report
    elif request.form.get('month_year'):
        # convert month name into number
        month_number = '{:02d}'.format(month_list.index(request.form.get('month')) + 1)
        # combine year and month into a date string
        start_date = request.form.get('month_year') + '-' + month_number + '-01'
        # get every booking details in a certain month
        details_list = sql_function.get_monthly_bookings(start_date)
        title = 'Monthly Report on {} {}'.format(request.form.get('month'), request.form.get('month_year'))
    # if the user chooses annual report
    elif request.form.get('year'):
        # get the ending date of the financial year
        start_date = request.form.get('year') + '-01-01'
        # get every booking details in a year
        details_list = sql_function.get_annual_bookings(start_date)
        title = 'Annual Report between 1st January {} and 31st December {}'.format(request.form.get('year'), request.form.get('year'))
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        # get number of maintenance and maintenance costs for each month
        for i in range(1, 13):
            number_list.append(0)
            hour_list.append(0)
        for i in range(0, len(month_list), 1):
            for detail in details_list:
                if detail['rental_start_datetime'].strftime('%Y-%m-%d')[5:7] == months[i]:
                    number_list[i] += 1
                    if detail['rental_start_datetime'].date() == detail['expected_return_datetime'].date():
                        hour_list[i] += 1
                    else:
                        difference = (detail['expected_return_datetime'].date() - detail['rental_start_datetime'].date()).days
                        hour_list[i] += difference
        # Reconstruct month_list
        months = []
        for i in range(1, 13, 1):
            string = calendar.month_name[i] + ' ' + request.form.get('year')
            months.append(string)
    # build up the category list
    for detail in details_list:
        if detail['category_name'] not in category_list:
            category_list.append(detail['category_name'])
            category_total_number.append(0)
            category_total_hour.append(0)
    # get number of booking and booking hours for each category
    for i in range(0, len(category_list), 1):
        for detail in details_list:
            if detail['category_name'] == category_list[i]:
                category_total_number[i] += 1
                total_number += 1
                # if rental start date is equal to end date, make it a day
                if detail['rental_start_datetime'].date() == detail['expected_return_datetime'].date():
                    category_total_hour[i] += 1
                    total_hour += 1
                else:
                    difference = (detail['expected_return_datetime'].date() - detail['rental_start_datetime'].date()).days
                    category_total_hour[i] += difference
                    total_hour += difference
    return render_template('admin/equipment_report.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg, month_flag=month_flag,
                           year_flag=year_flag, month_list=month_list, year_list=year_list, category_list=category_list,
                           category_total_number=category_total_number, category_total_hour=category_total_hour, total_number=total_number,
                           total_hour=total_hour, number_list=number_list, hour_list=hour_list, months=months, title=title)
