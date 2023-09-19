from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import mysql.connector
from app import config
import math
import re
import uuid
from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(config)
app.config['PERMANENT_SESSION_LIFETIME'] = 86400
app.secret_key = 'aHn6Zb7MstRxC8vEoF2zG3B9wQjKl5YD'
scheduler = APScheduler()
scheduler.init_app(app)
bcrypt = Bcrypt(app)

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
    db_conn = connection.cursor()
    return db_conn


def check_permissions():
    """
    Check user permissions based on session variables and return a permission level.

    Returns:
    - An integer representing the user's permission level:
        - 4 for root users.
        - 3 for admin users.
        - 2 for instructor users.
        - 1 for member users.
        - 0 for users with no specific role.

    This function examines session variables to determine a user's permissions.
    It assigns a numeric permission level based on the user's role, with higher values indicating higher access levels.
    If none of the specific roles are found, it returns 0 as the default permission level.

    Example:
    # Check user's permissions and assign a permission level
    permission_level = check_permissions()
    """
    is_member = session['is_member']
    is_instructor = session['is_instructor']
    is_admin = session['is_admin']
    is_root = session['is_root']
    if is_root == 1:
        return 4
    elif is_admin == 1:
        return 3
    elif is_instructor == 1:
        return 2
    elif is_member == 1:
        return 1
    else:
        return 0


def upload_image(file):
    """
    Uploads an image file and returns the URL of the uploaded image.

    Args:
    - file: The image file to be uploaded.

    Returns:
    - The URL of the uploaded image.

    This function generates a unique filename for the image using a UUID (Universally Unique Identifier).
    It saves the image to a specified directory and constructs the URL for accessing the uploaded image.
    The URL is generated based on the application's 'static' route and the filename.

    Example:
    # Upload an image and get its URL
    uploaded_image_url = upload_image(request.files['image'])
    """
    file_name = str(uuid.uuid4()) + '.jpg'
    file.save(f"./static/image/upload_image/{file_name}")
    # file.save(f"/home/leozhao95/mysite2/static/image/upload_image/{filename}")
    image_url = url_for('static', filename=f'image/upload_image/{file_name}')
    return image_url


def operate_sql(sql, values=None, fetch=1):
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
        cursor.close()
    return temp


region_list = operate_sql("""SELECT * FROM `region`;""")
title_list = operate_sql("""SELECT * FROM `title`;""")
city_list = operate_sql("""SELECT * FROM `city`;""")
question_list = operate_sql("""SELECT * FROM `security_question`;""")

from app import admin, member, root, guest
