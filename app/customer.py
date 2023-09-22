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
                    breadcrumbs.append({"text": str(sub).replace("-", " "), "url": "/products/" + str(category) + "/" + str(sub)})
                else:
                    msg = "Sorry, we can't find the page you're looking for!."
                    return render_template('guest/jump.html', goUrl='/', msg=msg)
        else:
            msg = "Sorry, we can't find the page you're looking for!."
            return render_template('guest/jump.html', goUrl='/', msg=msg)

    return render_template('customer/products.html', breadcrumbs=breadcrumbs)


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
    return render_template('customer/product_detail.html', detail_id=detail_id, breadcrumbs=breadcrumbs)
