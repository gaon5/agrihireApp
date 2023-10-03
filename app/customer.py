from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import re
from app import app, check_permissions, sql_function, bcrypt


@app.route('/equipments', defaults={'category': None, 'sub': None})
@app.route('/equipments/<category>', defaults={'sub': None})
@app.route('/equipments/<category>/<sub>')
def equipments(category, sub):
    breadcrumbs = [{"text": "Equipments", "url": "/equipments"}]
    sub_id = category_id = None
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
        if any(categories['name'] == category for categories in sql_function.category.values()):
            breadcrumbs.append({"text": str(category).replace("-", " "), "url": "/equipments/" + str(category)})
            category_id = next((key for key, value in sql_function.category.items() if value['name'] == category), None)
            if sub:
                if sub in sql_function.category[category_id]['subcategories']:
                    sub_id = next((item['sub_id'] for item in sql_function.sub_category_list if item['name'] == sub), None)
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
    else:
        sql_equipments, count = sql_function.get_all_equipment(sql_page)
    return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, category_list=sql_function.category_list,
                           count=count, msg=last_msg, error_msg=last_error_msg)


@app.route('/equipments/search_equipment', methods=['GET', 'POST'])
def search_equipment():
    breadcrumbs = [{"text": "Equipments", "url": "/equipments"}, {"text": "Search", "url": ""}]
    equipment = request.args.get('equipment')
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
        return render_template('customer/equipments.html', breadcrumbs=breadcrumbs, equipments=sql_equipments, category_list=sql_function.category_list,
                               count=count, msg=last_msg, error_msg=last_error_msg)
    else:
        session['error_msg'] = "Sorry, we can't find the page you're looking for!."
        return redirect(url_for('equipments'))


@app.route('/equipments/<category>/<sub>/detail', defaults={'detail_id': None})
@app.route('/equipments/<category>/<sub>/detail/<detail_id>', methods=['GET', 'POST'])
def equipment_detail(category, sub, detail_id):
    breadcrumbs = [{"text": "Equipments", "url": "/equipments"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if category:
        if any(categories['name'] == category for categories in sql_function.category.values()):
            breadcrumbs.append({"text": str(category).replace("-", " "), "url": "/equipments/" + str(category)})
            category_id = next((key for key, value in sql_function.category.items() if value['name'] == category), None)
            if sub:
                if sub in sql_function.category[category_id]['subcategories']:
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
    return render_template('customer/equipment_detail.html', detail_id=detail_id, breadcrumbs=breadcrumbs, equipment=equipment, msg=last_msg,
                           error_msg=last_error_msg)
