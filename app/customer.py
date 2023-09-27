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
            sql_equipments = sql_function.get_equipment_by_sub(sub_id)
        else:
            sql_equipments = sql_function.get_equipment_by_category(category_id)
    else:
        sql_equipments = sql_function.get_all_equipment()
    category_list = []
    for i in sql_function.category_list:
        category_list.append({'category_id': i['category_id'], 'name': i['name'].replace("-", " ")})
    return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, category_list=category_list)


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
