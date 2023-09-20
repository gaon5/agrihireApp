from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import re
from app import app, check_permissions, operate_sql, category_list, sub_category_list


@app.route('/products', defaults={'category': None, 'sub': None})
@app.route('/products/<category>', defaults={'sub': None})
@app.route('/products/<category>/<sub>')
def products(category, sub):
    breadcrumbs = [{"text": "Products", "url": "/products"}]
    if category:
        if category in category_list:
            breadcrumbs.append({"text": str(category).replace("-", " "), "url": "/products/" + str(category)})
            if sub:
                if sub in sub_category_list:
                    breadcrumbs.append({"text": str(sub).replace("-", " "), "url": "/products/" + str(category) + "/" + str(sub)})
                elif sub not in sub_category_list:
                    msg = "Sorry, we can't find the page you're looking for!."
                    return render_template('guest/jump.html', goUrl='/', msg=msg)
        elif category not in category_list:
            msg = "Sorry, we can't find the page you're looking for!."
            return render_template('guest/jump.html', goUrl='/', msg=msg)

    return render_template('customer/products.html', breadcrumbs=breadcrumbs)


@app.route('/product_detail', defaults={'detail_id': None})
@app.route('/product_detail/<detail_id>', methods=['GET', 'POST'])
def product_detail(detail_id):
    if not detail_id:
        msg = "Sorry, we can't find the page you're looking for!."
        return render_template('guest/jump.html', goUrl='/', msg=msg)
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
    return render_template('customer/product_detail.html', detail_id=detail_id)
