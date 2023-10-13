from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
from app import app, check_permissions, scheduler, sql_function


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
            sql_function.insert_category(new_category)
            last_msg = "New category added"
        # if the edit button is pressed, update the name of the category
        elif 'edit' in request.form:
            category_name = request.form['category_name']
            category_id = request.form['category_id']
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
    # category_list   category_list = operate_sql("""SELECT * FROM `category`;""", close=0)
    category_list = sql_function.category_list
    return render_template('admin/manage_category.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg,
                           category_list=category_list)


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
    # get every category from the database
    category_list = sql_function.get_categories()
    # get every sub category and respective main categories from the database
    subcategory_list = sql_function.get_main_and_sub_categories()
    return render_template('admin/manage_subcategory.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg,
                           subcategory_list=subcategory_list, category_list=category_list)


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
        if user_id:
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
        if user_id:
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
