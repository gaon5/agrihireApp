from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
from app import app, check_permissions, scheduler, bcrypt, sql_function


@app.route('/my_task')
@scheduler.task('interval', id='my_task', seconds=60)
def my_task():
    """
    This is a scheduled task
    :return:
    """
    pass


@app.route('/')
def index():
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    return render_template('guest/index.html', msg=last_msg, error_msg=last_error_msg)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    breadcrumbs = [{"text": "Login", "url": "/login/"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' in session:
        session['error_msg'] = 'You are already logged in.'
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        account = sql_function.get_account(email)
        if account is not None:
            user_detail = sql_function.get_user_detail(account['user_id'])
            if user_detail['state']:
                if bcrypt.check_password_hash(account['password'], password):
                    # Login successful
                    sql_function.set_last_login_date(account['user_id'])
                    session['loggedIn'] = True
                    session['user_id'] = account['user_id']
                    session['is_admin'] = account['is_admin']
                    session['is_customer'] = account['is_customer']
                    session['is_staff'] = account['is_staff']
                    session['msg'] = 'Login successful'
                    return redirect(url_for('index'))
                else:
                    # password error
                    last_error_msg = 'Email or password error.'
            else:
                last_error_msg = 'The account has been Inactivated, please get in touch with the staff.'
        else:
            # Email error
            last_error_msg = 'Email or password error.'
    return render_template('guest/login.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    if 'loggedIn' not in session:
        session['error_msg'] = 'You are already logout.'
        return redirect(url_for('index'))
    session.pop('loggedIn', None)
    session.pop('user_id', None)
    session.pop('is_admin', None)
    session.pop('is_customer', None)
    session.pop('is_staff', None)
    session['msg'] = "Logout successful!"
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    breadcrumbs = [{"text": "Register", "url": "/register"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    if 'loggedIn' in session:
        session['error_msg'] = 'You have to logout first.'
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Get data
        email = request.form.get('email')
        password = request.form.get('password')
        given_name = request.form.get('given_name')
        surname = request.form.get('surname')
        phone_number = request.form.get('phone_number')
        region_id = request.form.get('region_id')
        city_id = request.form.get('city_id')
        address = request.form.get('address')
        birth_date = request.form.get('birth_date')
        title = request.form.get('title')
        question = request.form.get('question')
        answer = request.form.get('answer')
        account = sql_function.get_account(email)
        if account:
            # Email already exists
            last_error_msg = 'Email already exists!'
            return render_template('guest/register.html', titles=sql_function.title_list, questions=sql_function.question_list,
                                   breadcrumbs=breadcrumbs, cities=sql_function.city_list, msg=last_msg, error_msg=last_error_msg)
        # Insert account data into database
        sql_function.register_account(email, password, title, given_name, surname, question, answer, phone_number, region_id, city_id, address, birth_date)
        session['msg'] = 'Registration success!'
        return redirect(url_for('login'))
    return render_template('guest/register.html', titles=sql_function.title_list, questions=sql_function.question_list, breadcrumbs=breadcrumbs,
                           regions=sql_function.region_list, cities=sql_function.city_list, msg=last_msg, error_msg=last_error_msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    breadcrumbs = [{"text": "Reset Password", "url": "/reset_password"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    email = request.form.get('email')
    if 'loggedIn' in session:
        session['error_msg'] = 'You are already logged in.'
        return redirect(url_for('index'))
    if email:
        account = sql_function.get_account(email)
        if not account:
            last_error_msg = "Didn't have this account!"
            return render_template('guest/reset_password.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)
        else:
            session['user_id'] = account['user_id']
            question = sql_function.get_customer_question(account['user_id'])
            return render_template('guest/answer.html', question=question, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)
    if request.method == 'POST':
        # Get data
        if 'user_id' in session:
            user_id = session['user_id']
            answer = request.form.get('answer')
            question = sql_function.get_customer_question(user_id)
            if not question['answer'] or (answer and question['answer'] and answer.lower() != question['answer'].lower()):
                last_error_msg = "The answer is incorrect!"
                return render_template('guest/answer.html', question=question, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)
            return redirect(url_for('change_password'))
    return render_template('guest/reset_password.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user_id = session['user_id']
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    breadcrumbs = [{"text": "Change Password", "url": "/change_password"}]
    if request.method == 'POST':
        session.pop('user_id', None)
        password = request.form.get('password')
        user_id = request.form.get('user_id')
        sql_function.set_password(password, user_id)
        session['msg'] = "Password reset successful!"
        return redirect(url_for('login'))
    return render_template('guest/change_password.html', user_id=user_id, breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    breadcrumbs = [{"text": "Dashboard", "url": "/dashboard"}]
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    # Number of customers, staff, equipment, bookings in the system
    customer_stat, staff_stat, equipment_stat, booking_stat = sql_function.stats_dashboard()
    if 'loggedIn' in session:
        # First determine whether to log in, then determine the user type, and then return different panels according to the type.
        if session['is_admin'] == 1:
            return render_template('admin/dashboard.html', breadcrumbs=breadcrumbs, customer_stat=customer_stat, staff_stat=staff_stat,
                                   equipment_stat=equipment_stat, booking_stat=booking_stat, msg=last_msg, error_msg=last_error_msg)
        elif session['is_staff'] == 1:
            return render_template('staff/dashboard.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)
        elif session['is_customer'] == 1:
            return redirect(url_for('index'))
            # breadcrumbs = [{"text": "Personal Center", "url": "#"}]
            # return render_template('customer/dashboard.html', breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)
        else:
            session['error_msg'] = 'Incorrect permissions'
            return redirect(url_for('index'))
    else:
        session['error_msg'] = 'Incorrect permissions'
        return redirect(url_for('index'))


# route for update information
@app.route('/edit_detail', methods=['GET', 'POST'])
def edit_detail():
    breadcrumbs = [{"text": "Edit My Detail", "url": "/edit_detail"}]
    if 'loggedIn' in session:
        user_id = session.get('user_id', '')
        last_msg = session.get('msg', '')
        last_error_msg = session.get('error_msg', '')
        session['msg'] = session['error_msg'] = ''
        permission_level = check_permissions()
        # Mapping to corresponding functions and templates
        details_function_map = {
            1: {"update": sql_function.update_customer_details, "template": "customer/update_information.html"},
            2: {"update": sql_function.update_staff_details, "template": "staff/update_information.html"},
            3: {"update": sql_function.update_admin_details, "template": "admin/update_information.html"}
        }
        if permission_level not in details_function_map:
            session['error_msg'] = 'Incorrect permissions'
            return redirect(url_for('index'))
        if request.method == 'POST':
            details_data = {
                "first_name": request.form.get('first_name').capitalize(),
                "last_name": request.form.get('last_name').capitalize(),
                "title": int(request.form.get('title')),
                "email": request.form.get('email'),
                "phone_number": request.form.get('phone_number'),
                "user_id": int(request.form.get('user_id'))
            }
            # Additional attributes for customers
            if permission_level == 1:
                details_data["birth_date"] = datetime.strptime(request.form.get('birth_date'), '%d %b %Y').strftime('%Y-%m-%d')
                details_data["region"] = int(request.form.get('region'))
                details_data["city"] = int(request.form.get('city'))
                details_data["street_name"] = request.form.get('street_name')
            email_result = sql_function.get_account(details_data["email"])
            if int(email_result['user_id']) != user_id:
                last_error_msg = "Email entered is already in use. Please enter another email address."
            else:
                details_function_map[permission_level]["update"](**details_data)
                last_msg = "Update successful"
        # Get the latest details
        details_list = sql_function.get_user_detail(user_id)
        if 'birth_date' in details_list:
            details_list['birth_date'] = details_list['birth_date'].strftime('%d %b %Y')
        return render_template(details_function_map[permission_level]["template"], details_list=details_list, title_list=sql_function.title_list,
                               breadcrumbs=breadcrumbs, city_list=sql_function.city_list, region_list=sql_function.region_list,
                               msg=last_msg, error_msg=last_error_msg)
    else:
        session['error_msg'] = 'Incorrect permissions'
        return redirect(url_for('index'))


@app.route('/user_change_password', methods=['GET', 'POST'])
def user_change_password():
    breadcrumbs = [{"text": "Edit My Detail", "url": "/edit_detail"}]
    if 'loggedIn' not in session:
        session['error_msg'] = 'Incorrect permissions'
        return redirect(url_for('index'))
    user_id = session["user_id"]
    permission_level = check_permissions()
    # Mapping to the corresponding templates
    template_map = {
        1: "customer/change_password.html",
        2: "staff/change_password.html",
        3: "admin/change_password.html"
    }
    if permission_level not in template_map:
        session['error_msg'] = 'Incorrect permissions'
        return redirect(url_for('index'))
    last_msg = session.get('msg', '')
    last_error_msg = session.get('error_msg', '')
    session['msg'] = session['error_msg'] = ''
    original_password = sql_function.get_account(user_id)['password'].encode('utf-8')
    if request.method == 'POST':
        old_password = request.form.get('old_pw').encode('utf-8')
        new_password = request.form.get('new_pw').encode('utf-8')
        if not bcrypt.check_password_hash(original_password, old_password):
            last_error_msg = "Incorrect old password. Please try again."
        elif bcrypt.check_password_hash(original_password, new_password):
            last_error_msg = "New password cannot be the same as previous password. Please try again"
        else:
            sql_function.update_password(new_password, user_id)
            last_msg = "Password changed."
    return render_template(template_map[permission_level], breadcrumbs=breadcrumbs, msg=last_msg, error_msg=last_error_msg)


@app.route("/guest_cart")
def guest_cart():
    if 'loggedIn' in session:
        if session['is_customer'] == 1:
            return render_template('customer/customer_cart.html')
    else:
        msg = 'Please Log In To View Cart'
        breadcrumbs = [{"text": "Login", "url": "/login"}]
        return render_template('guest/login.html', msg=msg, breadcrumbs=breadcrumbs)


@app.errorhandler(Exception)
def handle_error(error):
    """
    Receive all unexpected errors
    :param error:
    :return: error.html
    """
    print(error)
    return render_template('guest/error.html', permissions=check_permissions())
