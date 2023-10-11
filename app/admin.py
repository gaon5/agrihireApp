from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import re
from app import app, check_permissions, scheduler, sql_function, bcrypt

# route for managing categories
@app.route('/manage_category', methods=['GET', 'POST'])
def manage_category():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Manage Category", "url": "/manage_category"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' in session:
        if check_permissions() > 2:
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
            category_list = sql_function.get_categories()
            return render_template('admin/manage_category.html',breadcrumbs=breadcrumbs, last_msg=last_msg, 
                                   last_error_msg=last_error_msg, category_list=category_list)
        else:
            session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
            return redirect(url_for('index'))
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))
    

# route for managing categories
@app.route('/manage_subcategory', methods=['GET', 'POST'])
def manage_subcategory():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}, {"text": "Manage Sub Category", "url": "/manage_subcategory"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' in session:
        if check_permissions() > 2:
            # if method is POST ...
            if request.method == 'POST':
                # if add button is pressed, insert a new category
                if 'add' in request.form:
                    main_category_id = request.form['main_category_id']
                    new_sub_category = request.form['new_sub_category']
                    sql_function.insert_subcategory(main_category_id,new_sub_category)
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
            return render_template('admin/manage_subcategory.html',breadcrumbs=breadcrumbs, last_msg=last_msg, 
                                   last_error_msg=last_error_msg, subcategory_list=subcategory_list, category_list=category_list)
        else:
            session['error_msg'] = 'You are not authorized to access this page. Please login a different account.'
            return redirect(url_for('index'))
    else:
        session['error_msg'] = 'You are not logged in, please login first.'
        return redirect(url_for('login'))