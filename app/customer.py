from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import re
from app import app, check_permissions, sql_function


@app.route('/products', defaults={'category': None, 'sub': None})
@app.route('/products/<category>', defaults={'sub': None})
@app.route('/products/<category>/<sub>')
def products(category, sub):
    breadcrumbs = [{"text": "Products", "url": "/products"}]
    if category:
        if any(categories['name'] == category for categories in sql_function.category.values()):
            breadcrumbs.append({"text": str(category).replace("-", " "), "url": "/products/" + str(category)})
            category_id = next((key for key, value in sql_function.category.items() if value['name'] == category), None)
            if sub:
                if sub in sql_function.category[category_id]['subcategories']:
                    sub_id = next((item['sub_id'] for item in sql_function.sub_category_list if item['name'] == sub), None)
                    breadcrumbs.append({"text": str(sub).replace("-", " "), "url": "/products/" + str(category) + "/" + str(sub)})
                else:
                    msg = "Sorry, we can't find the page you're looking for!."
                    return render_template('guest/jump.html', goUrl='/', msg=msg)
        else:
            msg = "Sorry, we can't find the page you're looking for!."
            return render_template('guest/jump.html', goUrl='/', msg=msg)
    if category:
        if sub:
            products = sql_function.get_product_by_sub(sub_id)
        else:
            products = sql_function.get_product_by_category(category_id)
    else:
        products = sql_function.get_all_product()
    return render_template('customer/products.html', breadcrumbs=breadcrumbs, products=products)


@app.route('/products/<category>/<sub>/detail', defaults={'detail_id': None})
@app.route('/products/<category>/<sub>/detail/<detail_id>', methods=['GET', 'POST'])
def product_detail(category, sub, detail_id):
    breadcrumbs = [{"text": "Products", "url": "/products"}]
    if category:
        if any(categories['name'] == category for categories in sql_function.category.values()):
            breadcrumbs.append({"text": str(category).replace("-", " "), "url": "/products/" + str(category)})
            category_id = next((key for key, value in sql_function.category.items() if value['name'] == category), None)
            if sub:
                if sub in sql_function.category[category_id]['subcategories']:
                    breadcrumbs.append({"text": str(sub).replace("-", " "), "url": "/products/" + str(category) + "/" + str(sub)})
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

    product = sql_function.get_product_by_id(detail_id)
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
    return render_template('customer/product_detail.html', detail_id=detail_id, breadcrumbs=breadcrumbs, product=product)

# route for update information
@app.route('/customer_update_personal_info', methods=['GET','POST'])
def customer_update_personal_info():
    # get user_id from session
    # user_id = session["user_id"]
    user_id = 1
    # create message variables to display in templates
    error_msg = ''
    msg = ''
    # update personal information if user submits the form
    if request.method == 'POST':
        first_name = request.form.get('first_name').capitalize()
        last_name = request.form.get('last_name').capitalize()
        # convert string into datetime object
        birth_date = datetime.strptime(request.form.get('birth_date'),'%d %b %Y').strftime('%Y-%m-%d')
        title = int(request.form.get('title'))
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        region = int(request.form.get('region'))
        city = int(request.form.get('city'))
        street_name = request.form.get('street_name')
        user_id = int(request.form.get('user_id'))
        email_result = sql_function.check_customer_email(email)
        if int(email_result['user_id']) != user_id:
            error_msg = "Email entered is already in use. Please enter another email address."
        else:
            sql_function.update_customer_details(first_name, last_name, birth_date, title, phone_number, region, city, street_name,email,user_id)
            msg = "Update successful"
    # take latest details_list
    details_list = sql_function.get_customer_details(user_id)
    details_list['birth_date'] = details_list['birth_date'].strftime('%d %b %Y')
    title_list = sql_function.title_list
    region_list = sql_function.region_list
    city_list = sql_function.city_list
    return render_template('customer/update_personal_info.html', details_list=details_list, title_list=title_list, region_list=region_list, city_list=city_list, msg=msg, error_msg=error_msg)