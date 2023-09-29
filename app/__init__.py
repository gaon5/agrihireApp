from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import mysql.connector
from app import config
import re
import uuid
from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(config)
app.config['PERMANENT_SESSION_LIFETIME'] = 8640
app.secret_key = 'aHn6Zb7MstRxC8vEoF2zG3B9wQjKl5YD'
scheduler = APScheduler()
scheduler.init_app(app)
bcrypt = Bcrypt(app)


def check_permissions():
    """
    Check user permissions based on session variables and return a permission level.

    Returns:
    - An integer representing the user's permission level:
        - 3 for admin users.
        - 2 for staff users.
        - 1 for customer users.
        - 0 for users with no specific role.

    This function examines session variables to determine a user's permissions.
    It assigns a numeric permission level based on the user's role, with higher values indicating higher access levels.
    If none of the specific roles are found, it returns 0 as the default permission level.

    Example:
    # Check user's permissions and assign a permission level
    permission_level = check_permissions()
    """
    is_customer = session['is_customer']
    is_staff = session['is_staff']
    is_admin = session['is_admin']
    if is_admin == 1:
        return 3
    elif is_staff == 1:
        return 2
    elif is_customer == 1:
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


from app import admin, customer, guest, staff
