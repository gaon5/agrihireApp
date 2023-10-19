import mysql.connector
from app import config, bcrypt
from datetime import date, datetime, timedelta
import math

db_conn = None
connection = None


def get_cursor():
    global db_conn
    global connection
    connection = mysql.connector.connect(user=config.dbuser,
                                         password=config.dbpass,
                                         host=config.dbhost,
                                         database=config.dbname,
                                         autocommit=True)
    db_conn = connection.cursor(dictionary=True)
    return db_conn


def operate_sql(sql, values=None, fetch=1, close=1):
    """
    Execute an SQL query and return the query result.

    Args:
    - sql (str): The SQL query to execute.
    - values (tuple, optional): Parameter values for the SQL query to replace placeholders (optional).
    - fetch (int, optional): Specify the number of rows to retrieve in the query result.
      1 means retrieve a single row (default), 0 means retrieve a single row but do not fetch it,
      None means retrieve all rows (optional).

    Returns:
    - The query result, which can be a single row, multiple rows, or None, depending on the fetch parameter.

    Notes:
    - This function executes an SQL query and optionally replaces placeholders in the query with parameter values.
    - If the query starts with "SELECT," you can retrieve the query result based on the value of the fetch parameter.
    - If a MySQL database error occurs, it will be caught and printed as an exception.
    - Regardless of the outcome, the function will close the database cursor.

    Examples:
    # Execute a simple query
    result = operate_sql("SELECT * FROM users WHERE age > %s", (18,))

    # Execute a query and fetch a single row
    user = operate_sql("SELECT * FROM users WHERE username = %s", ("john_doe",), fetch=0)

    # Execute a query and fetch all results
    all_users = operate_sql("SELECT * FROM users")
    """
    temp = None
    try:
        cursor = get_cursor()
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        if sql.startswith("SELECT"):
            if fetch:
                temp = cursor.fetchall()
            else:
                temp = cursor.fetchone()
    except mysql.connector.Error as e:
        print("MySQL error:", e)
    finally:
        if close:
            cursor.close()
    return temp


region_list = operate_sql("""SELECT * FROM `region`;""", close=0)
title_list = operate_sql("""SELECT * FROM `title`;""", close=0)
city_list = operate_sql("""SELECT * FROM `city`;""", close=0)
question_list = operate_sql("""SELECT * FROM `security_question`;""", close=0)
category_list = operate_sql("""SELECT * FROM `category`;""", close=0)
sub_category_list = operate_sql("""SELECT * FROM `sub_category`;""", close=0)

category = {cat['category_id']: {'name': cat['name'], 'subcategories': []} for cat in category_list}
for sub in sub_category_list:
    categories = category[sub['category_id']]
    categories['subcategories'].append(sub['name'])


def get_staff_id(user_id):
    sql = """SELECT staff_id FROM staff WHERE user_id = %s"""
    staff_id = operate_sql(sql, (user_id,), fetch=0)['staff_id']
    return staff_id


def get_all_staff(page):
    sql = """SELECT staff_id,s.user_id AS user_id,title_id,first_name,last_name,phone_number,state,email,
                DATE_FORMAT(register_date,'%d %b %Y') AS register_date,DATE_FORMAT(last_login_date,'%d %b %Y') AS last_login_date from staff s
                LEFT JOIN user_account ua on ua.user_id = s.user_id
                WHERE state=1
                LIMIT %s, 15;"""
    staff_list = operate_sql(sql, (page,))
    sql = """SELECT COUNT(s.staff_id) AS count FROM staff s
                LEFT JOIN user_account ua on ua.user_id = s.user_id
                WHERE state=1;"""
    count = operate_sql(sql, fetch=0)
    count = math.ceil(count['count'] / 15)
    return staff_list, count


def search_staff(search, page):
    sqlSearch = "%" + search + "%"
    sql = """SELECT staff_id,s.user_id AS user_id,title_id,first_name,last_name,phone_number,state,email,
                DATE_FORMAT(register_date,'%d %b %Y') AS register_date,DATE_FORMAT(last_login_date,'%d %b %Y') AS last_login_date from staff s
                LEFT JOIN user_account ua on ua.user_id = s.user_id
                WHERE state=1 AND CONCAT(s.first_name, s.last_name, ua.email) LIKE %s
                LIMIT %s, 15;"""
    staff_list = operate_sql(sql, (sqlSearch, page,))
    sql = """SELECT COUNT(s.staff_id) AS count FROM staff s
                LEFT JOIN user_account ua on ua.user_id = s.user_id
                WHERE state=1 AND CONCAT(s.first_name, s.last_name, ua.email) LIKE %s;"""
    count = operate_sql(sql, (sqlSearch,), fetch=0)
    count = math.ceil(count['count'] / 15)
    return staff_list, count


def get_all_customer(page):
    sql = """SELECT customer_id,c.user_id AS user_id,title_id,first_name,last_name,phone_number,city_id,region_id,street_name,birth_date,
                question_id,answer,state,email,DATE_FORMAT(register_date,'%d %b %Y') AS register_date,
                DATE_FORMAT(last_login_date,'%d %b %Y') AS last_login_date from customer c
                LEFT JOIN user_account ua on ua.user_id = c.user_id
                WHERE state=1
                LIMIT %s, 15;"""
    customer_list = operate_sql(sql, (page,))
    sql = """SELECT COUNT(c.customer_id) AS count from customer c
                LEFT JOIN user_account ua on ua.user_id = c.user_id
                WHERE state=1;"""
    count = operate_sql(sql, fetch=0)
    count = math.ceil(count['count'] / 15)
    return customer_list, count


def search_customer(search, page):
    sqlSearch = "%" + search + "%"
    sql = """SELECT customer_id,c.user_id AS user_id,title_id,first_name,last_name,phone_number,city_id,region_id,street_name,birth_date,
                question_id,answer,state,email,DATE_FORMAT(register_date,'%d %b %Y') AS register_date,
                DATE_FORMAT(last_login_date,'%d %b %Y') AS last_login_date from customer c
                LEFT JOIN user_account ua on ua.user_id = c.user_id
                WHERE state=1 AND CONCAT(c.first_name, c.last_name, ua.email) LIKE %s
                LIMIT %s, 15;"""
    customer_list = operate_sql(sql, (sqlSearch, page,))
    sql = """SELECT COUNT(c.customer_id) AS count from customer c
                    LEFT JOIN user_account ua on ua.user_id = c.user_id
                    WHERE state=1 AND CONCAT(c.first_name, c.last_name, ua.email) LIKE %s;"""
    count = operate_sql(sql, (sqlSearch,), fetch=0)
    count = math.ceil(count['count'] / 15)
    return customer_list, count


def get_user_detail(user_id):
    sql = """SELECT ua.user_id, c.customer_id, title_id, first_name, last_name, email, phone_number, birth_date, region_id, city_id, street_name, c.state
            FROM user_account ua
            INNER JOIN customer c on c.user_id = ua.user_id
            WHERE ua.user_id = %s;"""
    details = operate_sql(sql, (user_id,), fetch=0)
    if details:
        return details
    sql = """SELECT ua.user_id, title_id, first_name, last_name, email, phone_number, s.state FROM user_account ua
                    INNER JOIN staff s on s.user_id = ua.user_id
                    WHERE ua.user_id = %s;"""
    details = operate_sql(sql, (user_id,), fetch=0)
    if details:
        return details
    sql = """SELECT ua.user_id, title_id, first_name, last_name, email, phone_number, a.state FROM user_account ua
                    INNER JOIN admin a on a.user_id = ua.user_id
                    WHERE ua.user_id = %s;"""
    details = operate_sql(sql, (user_id,), fetch=0)
    if details:
        return details


def get_equipment_id(instance_id):
    sql = """SELECT e.equipment_id FROM equipment AS e
                INNER JOIN equipment_instance AS ei ON ei.equipment_id = e.equipment_id
                WHERE instance_id = %s"""
    equipment_id = operate_sql(sql, (instance_id,), fetch=0)['equipment_id']
    return equipment_id


def get_account(email):
    sql = """SELECT * FROM user_account 
                WHERE email=%s;"""
    account = operate_sql(sql, (email,), fetch=0)
    return account


def set_last_login_date(user_id):
    today = datetime.today().date()
    sql = """UPDATE user_account 
                SET last_login_date=%s 
                WHERE user_id=%s"""
    operate_sql(sql, (today, user_id,))


def register_account(email, password, title, given_name, surname, question, answer, phone_number, region_id, city_id, address, birth_date):
    today = datetime.today().date()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    sql = """INSERT INTO user_account (email, password, is_customer, register_date, last_login_date) 
                VALUES (%s, %s, 1, %s, %s);"""
    operate_sql(sql, (email, hashed_password, today, today), close=0)
    account = operate_sql("""SELECT user_id from user_account WHERE email=%s;""", (email,), fetch=0, close=0)
    sql = """INSERT INTO customer (user_id,title_id,first_name,last_name,question_id,answer,state,phone_number,region_id,city_id,street_name,birth_date) 
                VALUES (%s,%s,%s,%s,%s,%s,1,%s,%s,%s,%s,%s);"""
    operate_sql(sql, (account['user_id'], title, given_name, surname, question, answer, phone_number, region_id, city_id, address, datetime.strptime(birth_date, '%Y-%m-%d').date()))


def get_customer_question(user_id):
    question = operate_sql("""SELECT sq.question_id,sq.question,c.answer FROM customer AS c 
                    LEFT OUTER JOIN security_question sq on sq.question_id = c.question_id WHERE user_id=%s;""", (user_id,), fetch=0)
    return question


def set_password(password, user_id):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    operate_sql("""UPDATE user_account SET password=%s WHERE user_id=%s;""", (hashed_password, user_id,))


def get_all_equipment(sql_page):
    sql = """SELECT e.equipment_id,ei.image_url,e.name,e.description,e.price,s.name AS sc_name,ca.name AS ca_name FROM equipment AS e
                LEFT JOIN classify c on e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s on c.sub_id = s.sub_id
                LEFT JOIN category ca on ca.category_id = s.category_id
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id
                WHERE ei.priority=1
                LIMIT %s, 12;"""
    equipment = operate_sql(sql, (sql_page,), close=0)
    sql = """SELECT COUNT(e.equipment_id) AS count FROM equipment e
                LEFT JOIN classify c on e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s on c.sub_id = s.sub_id
                LEFT JOIN category ca on ca.category_id = s.category_id
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id
                WHERE ei.priority=1;"""
    count = operate_sql(sql, fetch=0)
    count = math.ceil(count['count'] / 12)
    return equipment, count


def equipment_details():
    sql = """SELECT e.equipment_id, e.name AS e_name, e.price, e.count, e.length, e.width, e.height, e.requires_drive_license,e.description, 
                e.detail, ei.image_url, s.name AS sub_name, ca.name AS ca_name FROM equipment e 
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id  
                LEFT JOIN classify c on e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s on s.sub_id = c.sub_id
                LEFT JOIN category ca on ca.category_id = s.category_id
                WHERE ei.priority = 1
                ORDER BY ca.name;"""
    equipment_details = operate_sql(sql)
    return equipment_details


def get_equipment_by_search(search, sql_page):
    search = "%" + search + "%"
    sql = """SELECT e.equipment_id,ei.image_url,e.name,e.description,e.price,s.name AS sc_name,ca.name AS ca_name FROM equipment AS e
                LEFT JOIN classify c on e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s on c.sub_id = s.sub_id
                LEFT JOIN category ca on ca.category_id = s.category_id
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id
                WHERE ei.priority=1 AND e.name LIKE %s
                LIMIT %s, 12;"""
    equipment = operate_sql(sql, (search, sql_page,), close=0)
    sql = """SELECT COUNT(e.equipment_id) AS count FROM equipment e
                LEFT JOIN classify c on e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s on c.sub_id = s.sub_id
                LEFT JOIN category ca on ca.category_id = s.category_id
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id
                WHERE ei.priority=1  AND e.name LIKE %s;"""
    count = operate_sql(sql, (search,), fetch=0)
    count = math.ceil(count['count'] / 12)
    return equipment, count


def search_equipment_list(search):
    sql = """SELECT e.equipment_id, e.name AS e_name, e.price, e.count, e.length, e.width, e.height, e.requires_drive_license,e.description, 
                e.detail, ei.image_url, s.name AS sub_name, ca.name AS ca_name FROM equipment e 
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id  
                LEFT JOIN classify c on e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s on s.sub_id = c.sub_id
                LEFT JOIN category ca on ca.category_id = s.category_id
                WHERE e.name LIKE %s OR s.name LIKE %s OR ca.name LIKE %s"""
    result = operate_sql(sql, ('%' + search + '%', '%' + search + '%', '%' + search + '%',))
    return result


def get_equipment_by_category(category_id, sql_page):
    sql = """SELECT e.equipment_id,ei.image_url,e.name,e.description,e.price,s.name AS sc_name,ca.name AS ca_name FROM equipment e
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id
                LEFT JOIN classify c on e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s on s.sub_id = c.sub_id
                LEFT JOIN category ca on ca.category_id = s.category_id
                WHERE s.category_id=%s AND ei.priority=1
                LIMIT %s, 12;"""
    equipment = operate_sql(sql, (category_id, sql_page,), close=0)
    sql = """SELECT COUNT(e.equipment_id) AS count FROM equipment e
                LEFT JOIN equipment_img ei ON e.equipment_id = ei.equipment_id
                LEFT JOIN classify c ON e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s ON s.sub_id = c.sub_id
                LEFT JOIN category ca ON ca.category_id = s.category_id
                WHERE s.category_id = %s AND ei.priority = 1;"""
    count = operate_sql(sql, (category_id,), fetch=0)
    count = math.ceil(count['count'] / 12)
    return equipment, count


def get_equipment_by_sub(sub_id, sql_page):
    sql = """SELECT e.equipment_id,ei.image_url,e.name,e.description,e.price,s.name AS sc_name,ca.name AS ca_name FROM equipment e
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id
                LEFT JOIN classify c on e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s on s.sub_id = c.sub_id
                LEFT JOIN category ca on ca.category_id = s.category_id
                WHERE s.sub_id=%s AND ei.priority=1
                LIMIT %s, 12;"""
    equipment = operate_sql(sql, (sub_id, sql_page,), close=0)
    sql = """SELECT COUNT(e.equipment_id) AS count FROM equipment e
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id
                LEFT JOIN classify c on e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s on s.sub_id = c.sub_id
                LEFT JOIN category ca on ca.category_id = s.category_id
                WHERE s.sub_id=%s AND ei.priority=1;"""
    count = operate_sql(sql, (sub_id,), fetch=0)
    count = math.ceil(count['count'] / 12)
    return equipment, count


def get_equipment_by_id(equipment_id):
    sql = """SELECT * FROM equipment WHERE equipment_id=%s;"""
    equipment = operate_sql(sql, (equipment_id,))
    return equipment

def get_image_by_id(equipment_id):
    sql_img = """SELECT * FROM equipment_img WHERE equipment_id = %s;"""
    image = operate_sql(sql_img, (equipment_id,))
    return image


def get_equipment_by_wishlist(user_id, sql_page):
    sql = """SELECT e.equipment_id,ei.image_url,e.name,e.description,e.price,s.name AS sc_name,ca.name AS ca_name FROM customer
                LEFT JOIN wishlist w ON customer.customer_id = w.customer_id
                LEFT JOIN equipment e ON e.equipment_id = w.equipment_id
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id
                LEFT JOIN classify c on e.equipment_id = c.equipment_id
                LEFT JOIN sub_category s on s.sub_id = c.sub_id
                LEFT JOIN category ca on ca.category_id = s.category_id
                WHERE customer.user_id=%s AND ei.priority=1
                LIMIT %s, 15;;"""
    equipment = operate_sql(sql, (user_id, sql_page,), close=0)
    sql = """SELECT COUNT(e.equipment_id) AS count FROM customer
                    LEFT JOIN wishlist w ON customer.customer_id = w.customer_id
                    LEFT JOIN equipment e ON e.equipment_id = w.equipment_id
                    LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id
                    LEFT JOIN classify c on e.equipment_id = c.equipment_id
                    LEFT JOIN sub_category s on s.sub_id = c.sub_id
                    LEFT JOIN category ca on ca.category_id = s.category_id
                    WHERE customer.user_id=%s AND ei.priority=1;"""
    count = operate_sql(sql, (user_id,), fetch=0)
    count = math.ceil(count['count'] / 15)
    return equipment, count


def get_wishlist(user_id):
    sql = """SELECT ua.user_id, c.customer_id
                FROM user_account ua
                INNER JOIN customer c on c.user_id = ua.user_id
                WHERE ua.user_id = %s;"""
    customer = operate_sql(sql, (user_id,), fetch=0, close=0)
    customer_id = customer['customer_id']
    sql = """SELECT * FROM wishlist WHERE customer_id=%s;"""
    wishlist = operate_sql(sql, (customer_id,))
    return wishlist


def get_user_wishlist(user_id, equipment_id):
    sql = """SELECT ua.user_id, c.customer_id
                FROM user_account ua
                INNER JOIN customer c on c.user_id = ua.user_id
                WHERE ua.user_id = %s;"""
    customer = operate_sql(sql, (user_id,), fetch=0, close=0)
    customer_id = customer['customer_id']
    sql = """SELECT * FROM wishlist WHERE customer_id=%s AND equipment_id=%s;"""
    wishlist = operate_sql(sql, (customer_id, equipment_id,))
    return wishlist


def add_wishlist(user_id, equipment_id):
    sql = """SELECT ua.user_id, c.customer_id
                FROM user_account ua
                INNER JOIN customer c on c.user_id = ua.user_id
                WHERE ua.user_id = %s;"""
    customer = operate_sql(sql, (user_id,), fetch=0, close=0)
    customer_id = customer['customer_id']
    sql = """INSERT INTO wishlist (customer_id, equipment_id) VALUE (%s,%s);"""
    operate_sql(sql, (customer_id, equipment_id,))


def delete_wishlist(user_id, equipment_id):
    sql = """SELECT ua.user_id, c.customer_id
                FROM user_account ua
                INNER JOIN customer c on c.user_id = ua.user_id
                WHERE ua.user_id = %s;"""
    customer = operate_sql(sql, (user_id,), fetch=0, close=0)
    customer_id = customer['customer_id']
    sql = """DELETE FROM wishlist WHERE customer_id=%s AND equipment_id=%s;"""
    operate_sql(sql, (customer_id, equipment_id,))


def get_account_by_id(user_id):
    sql = """SELECT user_id, password FROM `user_account`
                WHERE user_id=%s;"""
    password = operate_sql(sql, (user_id,), fetch=0)
    return password


def update_password(password, user_id):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    sql = "UPDATE user_account SET password=%s WHERE user_id=%s"
    operate_sql(sql, (hashed_password, user_id))


def update_customer_details(first_name, last_name, birth_date, title, phone_number, region, city, street_name, email, user_id):
    sql = """UPDATE `customer` SET first_name=%s,last_name=%s,birth_date=%s,title_id=%s,phone_number=%s,region_id=%s,city_id=%s,street_name=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (first_name, last_name, birth_date, title, phone_number, region, city, street_name, user_id), close=0)
    sql = """UPDATE `user_account` SET email=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (email, user_id))


def add_customer(first_name, last_name, birth_date, title, phone_number, region, city, street_name, email, password):
    register_account(email, password, title, last_name, first_name, 1, "1", phone_number, region, city, street_name, birth_date)


def delete_customer(user_id):
    sql = """UPDATE customer SET state=0 Where user_id=%s"""
    operate_sql(sql, (user_id,))


def update_staff_details(first_name, last_name, title, phone_number, email, user_id):
    sql = """UPDATE `staff` SET first_name=%s,last_name=%s,title_id=%s,phone_number=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (first_name, last_name, title, phone_number, user_id), close=0)
    sql = """UPDATE `user_account` SET email=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (email, user_id))


def add_staff(first_name, last_name, title, phone_number, email, password):
    today = datetime.today().date()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    sql = """INSERT INTO user_account (email, password, is_staff, register_date, last_login_date) 
                    VALUES (%s, %s, 1, %s, %s);"""
    operate_sql(sql, (email, hashed_password, today, today), close=0)
    account = operate_sql("""SELECT user_id from user_account WHERE email=%s;""", (email,), fetch=0, close=0)
    sql = """INSERT INTO staff (user_id,title_id,first_name,last_name,phone_number,state) 
                    VALUES (%s,%s,%s,%s,%s,1);"""
    operate_sql(sql, (account['user_id'], title, first_name, last_name, phone_number,))


def delete_staff(user_id):
    sql = """UPDATE staff SET state=0 Where user_id=%s"""
    operate_sql(sql, (user_id,))


def update_admin_details(first_name, last_name, title, phone_number, email, user_id):
    sql = """UPDATE `admin` SET first_name=%s,last_name=%s,title_id=%s,phone_number=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (first_name, last_name, title, phone_number, user_id), close=0)
    sql = """UPDATE `user_account` SET email=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (email, user_id))


def stats_dashboard():
    customer_stat = operate_sql("""SELECT COUNT(customer_id) FROM hire.customer WHERE state = 1;""", close=0)
    staff_stat = operate_sql("""SELECT COUNT(staff_id) FROM hire.staff WHERE state = 1;""", close=0)
    equipment_stat = operate_sql("""SELECT COUNT(equipment_id) FROM hire.equipment;""", close=0)
    booking_stat = operate_sql("""SELECT COUNT(log_id) FROM hire.hire_log;""")
    return customer_stat, staff_stat, equipment_stat, booking_stat


def get_bookings(user_id):
    sql = """SELECT ua.user_id, c.customer_id
                    FROM user_account ua
                    INNER JOIN customer c on c.user_id = ua.user_id
                    WHERE ua.user_id = %s;"""
    customer = operate_sql(sql, (user_id,), fetch=0, close=0)
    customer_id = customer['customer_id']
    sql = """SELECT hi.hire_id, hi.instance_id, hl.datetime, e.name, ers.rental_start_datetime, e.price, ers.expected_return_datetime 
        FROM customer AS c 
        INNER JOIN hire_list AS hl ON c.customer_id = hl.customer_id
        INNER JOIN hire_item AS hi ON hl.hire_id = hi.hire_id
        INNER JOIN equipment_instance AS ei ON hi.instance_id = ei.instance_id
        INNER JOIN equipment_rental_status AS ers ON ers.instance_id = hi.instance_id
        INNER JOIN equipment AS e ON e.equipment_id = ei.equipment_id
        WHERE c.customer_id=%s;"""
    bookings = operate_sql(sql, (customer_id,))
    return bookings


def sql_delete_booking(instance_id=None, hire_id=None):
    if instance_id:
        sql = """DELETE FROM hire_item WHERE instance_id=%s;"""
        operate_sql(sql, (instance_id,))
        
        sql = """DELETE FROM equipment_rental_status WHERE instance_id=%s"""
        operate_sql(sql, (instance_id,))
    
    if hire_id:
        sql = """DELETE FROM hire_list WHERE hire_id=%s"""
        operate_sql(sql, (hire_id,))


def update_booking_end_date(instance_id, new_end_date):
    sql = """UPDATE equipment_rental_status SET expected_return_date=%s WHERE instance_id=%s;"""
    operate_sql(sql, (new_end_date, instance_id))


def get_pickup_equipment(the_date):
    sql = """SELECT ers.equipment_rental_status_id, ers.instance_id, name, customer_id, TIME(rental_start_datetime) AS rental_start_datetime, notes FROM hire.equipment_rental_status AS ers
                INNER JOIN equipment_instance AS ei ON ei.instance_id = ers.instance_id
                INNER JOIN equipment AS e ON e.equipment_id = ei.equipment_id
                WHERE (rental_status_id = 1) AND (DATE(rental_start_datetime) = %s)
                ORDER BY rental_start_datetime"""
    pickup_list = operate_sql(sql, (the_date,))
    return pickup_list


def check_out_equipment(equipment_rental_status_id, instance_id, user_id, current_datetime):
    # update the rental status of a booking
    sql = "UPDATE equipment_rental_status SET rental_status_id = 2 WHERE equipment_rental_status_id = %s;"
    operate_sql(sql, (equipment_rental_status_id,))
    # get staff id from user id
    staff_id = get_staff_id(user_id)
    # get equipment id from instance id
    equipment_id = get_equipment_id(instance_id)
    # insert hire log the necessary details
    sql = """INSERT INTO hire_log (log_id, staff_id, datetime, equipment_status_id, message, equipment_id) 
            VALUES (NULL, %s, %s, 1, 'Equipment hired to a customer', %s);"""
    operate_sql(sql, (staff_id, current_datetime, equipment_id))


def get_return_equipment(the_date):
    sql = """SELECT ers.equipment_rental_status_id, ers.instance_id, name, customer_id, TIME(expected_return_datetime) AS expected_return_datetime, notes FROM hire.equipment_rental_status AS ers
                INNER JOIN equipment_instance AS ei ON ei.instance_id = ers.instance_id
                INNER JOIN equipment AS e ON e.equipment_id = ei.equipment_id
                WHERE (rental_status_id = 2) AND (DATE(expected_return_datetime) = %s)
                ORDER BY expected_return_datetime"""
    return_list = operate_sql(sql, (the_date,))
    return return_list


def return_equipment(equipment_rental_status_id, instance_id, user_id, current_datetime):
    # get expected return datetime
    sql = """SELECT expected_return_datetime AS expected_return_datetime FROM equipment_rental_status WHERE equipment_rental_status_id = %s"""
    expected_return_datetime = operate_sql(sql, (equipment_rental_status_id,), fetch=0)['expected_return_datetime']
    # if the equipment is overdue, change status to overdue
    if current_datetime > expected_return_datetime:
        rental_status_id = 4
    # otherwise, change status to due on time
    else:
        rental_status_id = 3
    # update rental status
    sql = """UPDATE equipment_rental_status 
                SET rental_status_id = %s, actual_return_datetime = %s
                WHERE equipment_rental_status_id = %s"""
    operate_sql(sql, (rental_status_id, current_datetime, equipment_rental_status_id))
    # get staff id from user id
    staff_id = get_staff_id(user_id)
    # get equipment id from instance id
    equipment_id = get_equipment_id(instance_id)
    # insert hire log the necessary details
    sql = """INSERT INTO hire_log (log_id, staff_id, datetime, equipment_status_id, message, equipment_id) 
            VALUES (NULL, %s, %s, 3, 'Equipment returned from a customer', %s);"""
    operate_sql(sql, (staff_id, current_datetime, equipment_id))
    # update equipment's rental status to available
    sql = """UPDATE equipment_instance 
                SET instance_status = 1
                WHERE instance_id = %s"""
    operate_sql(sql, (instance_id,))


def updating_equipment_image(image_url, equipment_id):
    sql_img = """UPDATE hire.equipment_img SET image_url =%s WHERE equipment_id = %s"""
    operate_sql(sql_img, (equipment_id, image_url))


def updating_equipment(name, price, count, requires_drive_license, length, width, height, description, detail, equipment_id):
    sql = """UPDATE hire.equipment SET name = %s, price = %s, count = %s, requires_drive_license = %s, length = %s, width = %s, 
                height = %s, description = %s, detail = %s
                WHERE equipment_id= %s"""
    operate_sql(sql, (name, price, count, requires_drive_license, length, width, height, description, detail, equipment_id))

def add_equipment(name, price, count,length, width, height, requires_drive_license, min_stock_threshold, description, detail, image_url, priority):
    sql_data = get_cursor()
    sql = """INSERT INTO hire.equipment(name, price, count, priority, length, width, height, requires_drive_license, min_stock_threshold, description, 
            detail) VALUES (%s, %s, %s, 0, %s, %s, %s, %s, %s, %s, %s);"""
    value = (name, price, count ,length, width, height, requires_drive_license, min_stock_threshold, description, detail)
    sql_data.execute(sql, value)
    sql_data.execute("""SET @equipment_id = LAST_INSERT_ID();""")
    sql = """INSERT INTO hire.equipment_img(equipment_id, image_url, priority) VALUES (LAST_INSERT_ID(), %s, %s);"""
    value = (image_url, priority)
    sql_data.execute(sql, value)
    # sql = """INSERT INTO hire.equipment_instance(equipment_id, instance_status) VALUES (LAST_INSERT_ID(), 1)"""
    # sql_data.execute(sql)


def deleting_equipment(equipment_id):
    sql_img = "DELETE FROM hire.equipment_img WHERE equipment_id = %s;"
    operate_sql(sql_img, (equipment_id,))
    sql_equipment = "DELETE FROM hire.equipment WHERE equipment_id = %s;"
    operate_sql(sql_equipment, (equipment_id,))

def add_staff(first_name, last_name, title, phone_number, email, password):
    today = datetime.today().date()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    sql = """INSERT INTO user_account (email, password, is_staff, register_date, last_login_date) 
                    VALUES (%s, %s, 1, %s, %s);"""
    operate_sql(sql, (email, hashed_password, today, today), close=0)
    account = operate_sql("""SELECT user_id from user_account WHERE email=%s;""", (email,), fetch=0, close=0)
    sql = """INSERT INTO staff (user_id,title_id,first_name,last_name,phone_number,state) 
                    VALUES (%s,%s,%s,%s,%s,1);"""
    operate_sql(sql, (account['user_id'], title, first_name, last_name, phone_number,))

def get_maintenance_equipment(today_date):
    details = operate_sql("""SELECT * FROM `equipment_maintenance`;""", close=0)
    # set status to overdue if the maintenance is not completed and the expected return date is in the past
    sql = """UPDATE equipment_maintenance SET maintenance_status_id=2
                WHERE instance_id=%s"""
    for detail in details:
        if detail['maintenance_end_date'] < today_date and detail['maintenance_status_id'] != 3:
            operate_sql(sql, (detail['instance_id'],))
    # get every detail of each equipment under maintenance
    sql = """SELECT instance_id, maintenance_start_date AS start_date, maintenance_end_date AS end_date, maintenance_type.name AS type, maintenance_status.name AS status, notes FROM equipment_maintenance
                INNER JOIN maintenance_type ON maintenance_type.maintenance_type_id = equipment_maintenance.maintenance_type_id
                INNER JOIN maintenance_status ON maintenance_status.maintenance_status_id = equipment_maintenance.maintenance_status_id
                WHERE NOT equipment_maintenance.maintenance_status_id = 3
                ORDER BY maintenance_start_date;"""
    details = operate_sql(sql)
    return details


def complete_maintenance(id):
    # update instance's status in the equipment_maintenance table
    sql="""UPDATE equipment_maintenance SET maintenance_status_id=3
            WHERE instance_id=%s"""
    operate_sql(sql, (id,))
    # update instance's status to available
    sql="""UPDATE equipment_instance SET instance_status=1
            WHERE instance_id=%s"""
    operate_sql(sql, (id,))

# call a function to get category list so that the website always display LATEST information (don't delete this )
def get_category_list():
    category_list = operate_sql("""SELECT * FROM `category`;""", close=0)
    return category_list

def insert_category(value):
    sql = """INSERT INTO category (category_id, name) VALUES (NULL, %s)"""
    operate_sql(sql, (value,))

def check_category(id):
    sql="""SELECT * FROM category
            INNER JOIN sub_category ON sub_category.category_id = category.category_id
            WHERE category.category_id = %s;"""
    details = operate_sql(sql, (id,))
    return details

def validate_category(input):
    category_list = operate_sql("""SELECT * FROM `category`;""", close=0)
    result = False
    for category in category_list:
        if input.lower() == category['name'].lower():
            result = True
    return result

def edit_category(id, name):
    sql = """UPDATE category 
                SET name = %s
                WHERE category_id = %s"""
    operate_sql(sql, (name,id))

def delete_category(id):
    sql = """DELETE FROM category WHERE category_id=%s"""
    operate_sql(sql, (id,))


def get_main_and_sub_categories():
    sql = """SELECT sub_id, sub_category.name AS sub, category.category_id, category.name AS main FROM sub_category 
                INNER JOIN category ON category.category_id = sub_category.category_id
                ORDER BY sub_category.name"""
    details = operate_sql(sql)
    return details

def insert_subcategory(id, name):
    sql="""INSERT INTO sub_category (sub_id, category_id, name) VALUES (NULL, %s, %s)"""
    operate_sql(sql, (id, name))


def check_subcategory(id):
    sql="""SELECT * FROM sub_category 
            INNER JOIN classify ON classify.sub_id = sub_category.sub_id
            WHERE sub_category.sub_id = %s"""
    details = operate_sql(sql, (id,))
    return details

def validate_subcategory(input, category_id):
    sub_category_list = operate_sql("""SELECT * FROM `sub_category`;""", close=0)
    result = False
    for sub in sub_category_list:
        if sub['category_id'] == int(category_id) and sub['name'].lower() == input.lower():
            result = True
    return result

def change_category(sub_id, main_id):
    sql = """UPDATE sub_category 
                SET category_id = %s
                WHERE sub_id = %s"""
    operate_sql(sql, (main_id, sub_id))


def edit_subcategory(id, name):
    sql = """UPDATE sub_category 
                SET name = %s
                WHERE sub_id = %s"""
    operate_sql(sql, (name,id))


def delete_subcategory(id):
    sql = """DELETE FROM sub_category WHERE sub_id=%s"""
    operate_sql(sql, (id,))


def customer_list():
    sql = """SELECT CONCAT(c.first_name," ",c.last_name) AS Customer, c.phone_number, e.name AS Equipment, rs.name AS Status, 
                DATE(ers.rental_start_datetime) AS sDate, TIME(ers.rental_start_datetime) AS sTime, DATE(ers.expected_return_datetime) AS rDate, 
                TIME(ers.expected_return_datetime) AS rTime, DATE(actual_return_datetime) AS aDate, TIME(actual_return_datetime) AS aTime
                FROM hire.equipment_rental_status ers
                INNER JOIN customer c ON c.customer_id = ers.customer_id
                INNER JOIN rental_status rs ON ers.rental_status_id = rs.rental_status_id
                INNER JOIN equipment_instance AS ei ON ei.instance_id = ers.instance_id
                INNER JOIN equipment AS e ON e.equipment_id = ei.equipment_id
                ORDER BY ers.expected_return_datetime ASC;"""
    equipment = operate_sql(sql)
    return equipment


def add_equipment_into_cart(user_id, equipment_id, count, start_time, end_time):
    sql = """SELECT ua.user_id, c.customer_id
                FROM user_account ua
                INNER JOIN customer c on c.user_id = ua.user_id
                WHERE ua.user_id = %s;"""
    customer = operate_sql(sql, (user_id,), fetch=0, close=0)
    customer_id = customer['customer_id']
    sql = """INSERT INTO shopping_cart_item (customer_id,equipment_id,count,start_time,end_time)
            VALUES (%s,%s,%s,%s,%s)"""
    # print(sql % (customer_id,equipment_id,count,start_time,duration))
    operate_sql(sql, (customer_id, equipment_id, count, start_time, end_time,))


def sql_delete_item(cart_item_id):
    sql = """DELETE FROM shopping_cart_item WHERE cart_item_id=%s"""
    operate_sql(sql, (cart_item_id,))


def my_cart(user_id):
    sql = """SELECT ua.user_id, c.customer_id
                FROM user_account ua
                INNER JOIN customer c on c.user_id = ua.user_id
                WHERE ua.user_id = %s;"""
    customer = operate_sql(sql, (user_id,), fetch=0, close=0)
    customer_id = customer['customer_id']
    sql = """SELECT * FROM hire.shopping_cart_item as sci
                inner join equipment as e on sci.equipment_id = e.equipment_id
                LEFT JOIN equipment_img as ei on e.equipment_id = ei.equipment_id
                LEFT JOIN classify as c on e.equipment_id = c.equipment_id
                WHERE sci.customer_id = %s;"""
    # print(sql % (customer_id,equipment_id,count,start_time,duration))
    equipment_in_cart = operate_sql(sql, (customer_id,))
    return equipment_in_cart


def max_count(equipment_id):
    sql = """SELECT count(*) FROM hire.equipment_instance
                where equipment_id = %s and instance_status = 1;"""
    max_count = operate_sql(sql, (equipment_id,))
    max_amount = list(max_count[0].values())[0]
    return max_amount


def edit_equipment_in_cart(user_id, cart_item_id, quantity, start_time, end_time):
    sql = """SELECT ua.user_id, c.customer_id
                FROM user_account ua
                INNER JOIN customer c on c.user_id = ua.user_id
                WHERE ua.user_id = %s;"""
    customer = operate_sql(sql, (user_id,), fetch=0, close=0)
    customer_id = customer['customer_id']
    sql = """UPDATE shopping_cart_item 
                    SET count = %s, start_time = %s, end_time = %s
                    WHERE (customer_id = %s) and (cart_item_id = %s)"""
    # print(sql % (customer_id,equipment_id,count,start_time,duration))
    operate_sql(sql, (quantity, start_time, end_time, customer_id, cart_item_id,))
