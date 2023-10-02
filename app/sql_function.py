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


user_list = operate_sql("""SELECT * FROM `user_account`;""")
region_list = operate_sql("""SELECT * FROM `region`;""")
title_list = operate_sql("""SELECT * FROM `title`;""")
city_list = operate_sql("""SELECT * FROM `city`;""")
question_list = operate_sql("""SELECT * FROM `security_question`;""")
category_list = operate_sql("""SELECT * FROM `category`;""")
sub_category_list = operate_sql("""SELECT * FROM `sub_category`;""")

category = {cat['category_id']: {'name': cat['name'], 'subcategories': []} for cat in category_list}
for sub in sub_category_list:
    categories = category[sub['category_id']]
    categories['subcategories'].append(sub['name'])


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


def register_account(email, password, title, given_name, surname, question, answer):
    today = datetime.today().date()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    sql = """INSERT INTO user_account (email, password, is_customer, register_date, last_login_date) 
                VALUES (%s, %s, 1, %s, %s);"""
    operate_sql(sql, (email, hashed_password, today, today), close=0)
    account = operate_sql("""SELECT user_id from user_account WHERE email=%s;""", (email,), fetch=0, close=0)
    sql = """INSERT INTO customer (user_id,title_id,first_name,last_name,question_id,answer,state) 
                VALUES (%s,%s,%s,%s,%s,%s,1);"""
    operate_sql(sql, (account['user_id'], title, given_name, surname, question, answer), close=0)


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
    sql = """SELECT * FROM equipment e
                LEFT JOIN equipment_img ei on e.equipment_id = ei.equipment_id
                WHERE e.equipment_id=%s;"""
    equipment = operate_sql(sql, (equipment_id,))
    return equipment


def get_all_product():
    sql = """SELECT * FROM product AS p LEFT JOIN product_img pi on p.product_id = pi.product_id WHERE pi.priority=1;"""
    product = operate_sql(sql)
    return product


def get_product_by_category(category_id):
    sql = """SELECT * FROM product p
                LEFT JOIN product_img pi on p.product_id = pi.product_id
                LEFT JOIN classify c on p.product_id = c.product_id
                LEFT JOIN sub_category sc on sc.sub_id = c.sub_id
                WHERE sc.category_id=%s AND pi.priority=1;"""
    product = operate_sql(sql, (category_id,))
    return product


def get_product_by_sub(sub_id):
    sql = """SELECT * FROM product p
                LEFT JOIN product_img pi on p.product_id = pi.product_id
                LEFT JOIN classify c on p.product_id = c.product_id
                LEFT JOIN sub_category sc on sc.sub_id = c.sub_id
                WHERE sc.sub_id=%s AND pi.priority=1;"""
    product = operate_sql(sql, (sub_id,))
    return product


def get_product_by_id(product_id):
    sql = """SELECT * FROM product p
                LEFT JOIN product_img pi on p.product_id = pi.product_id
                WHERE p.product_id=%s AND pi.priority=1;"""
    product = operate_sql(sql, (product_id,), fetch=0)
    return product


def get_account_by_id(user_id):
    sql = """SELECT user_id, password FROM `user_account`
                WHERE user_id=%s;"""
    password = operate_sql(sql, (user_id,), fetch=0)
    return password


def update_password(password, user_id):
    sql = "UPDATE user_account SET password=%s WHERE user_id=%s"
    operate_sql(sql, (password, user_id))


def get_customer_details(user_id):
    sql = """SELECT ua.user_id, title_id, first_name, last_name, email, phone_number, birth_date, region_id, city_id, street_name FROM user_account ua
                INNER JOIN customer c on c.user_id = ua.user_id
                WHERE ua.user_id = %s;"""
    details = operate_sql(sql, (user_id,), fetch=0)
    return details


def update_customer_details(first_name, last_name, birth_date, title, phone_number, region, city, street_name, email, user_id):
    sql = """UPDATE `customer` SET first_name=%s,last_name=%s,birth_date=%s,title_id=%s,phone_number=%s,region_id=%s,city_id=%s,street_name=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (first_name, last_name, birth_date, title, phone_number, region, city, street_name, user_id))
    sql = """UPDATE `user_account` SET email=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (email, user_id))


def get_staff_details(user_id):
    sql = """SELECT ua.user_id, title_id, first_name, last_name, email, phone_number FROM user_account ua
                INNER JOIN staff s on s.user_id = ua.user_id
                WHERE ua.user_id = %s;"""
    details = operate_sql(sql, (user_id,), fetch=0)
    return details


def update_staff_details(first_name, last_name, title, phone_number, email, user_id):
    sql = """UPDATE `staff` SET first_name=%s,last_name=%s,title_id=%s,phone_number=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (first_name, last_name, title, phone_number, user_id))
    sql = """UPDATE `user_account` SET email=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (email, user_id))


def get_admin_details(user_id):
    sql = """SELECT ua.user_id, title_id, first_name, last_name, email, phone_number FROM user_account ua
                INNER JOIN admin a on a.user_id = ua.user_id
                WHERE ua.user_id = %s;"""
    details = operate_sql(sql, (user_id,), fetch=0)
    return details


def update_admin_details(first_name, last_name, title, phone_number, email, user_id):
    sql = """UPDATE `admin` SET first_name=%s,last_name=%s,title_id=%s,phone_number=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (first_name, last_name, title, phone_number, user_id))
    sql = """UPDATE `user_account` SET email=%s
                WHERE user_id=%s;"""
    operate_sql(sql, (email, user_id))
def stats_customers():
    sql = """SELECT COUNT(customer_id) FROM hire.customer WHERE state = 1;"""
    customer_stat = operate_sql(sql)
    return customer_stat

def stats_staff():
    sql = """SELECT COUNT(staff_id) FROM hire.staff WHERE state = 1;"""
    staff_stat = operate_sql(sql)
    return staff_stat

def stats_equipment():
    sql = """SELECT COUNT(equipment_id) FROM hire.equipment;"""
    equipment_stat = operate_sql(sql)
    return equipment_stat

def stats_booking():
    sql = """SELECT COUNT(log_id) FROM hire.hire_log;"""
    booking_stat = operate_sql(sql)
    return booking_stat
