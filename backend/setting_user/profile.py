from flask import render_template, session, request, redirect, url_for
from backend.db_connection import connect_aep_portal, connect_aep_DB
from datetime import datetime
from flask import current_app as app
import os
from PIL import Image
from werkzeug.utils import secure_filename
from backend.db_connection import connect_aep_portal

def update_profile():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    if 'username' not in session:
        return redirect(url_for('login'))

    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    username = session['username']
    mock_user_data = (
        "Thanapurt",
        "Sopon",
        "Tung",
        "thanapurt.sop@gmail.com",
        "SM001",
        "IT Department",
        "Senior Developer",
        "Active",
        "MD001",
        "john.jpg"
    )

    one_name, two_name, three_name, rps_email, rps_employee_id, rps_dpm, rps_level, rps_status, rps_modual, rps_photo = mock_user_data

    photo_path = os.path.join('static', 'picture', rps_photo)
    if os.path.exists(photo_path):
        photo_url = url_for('static', filename=f'picture/{rps_photo}')
    else:
        photo_url = url_for('static', filename='img/test1.jpg')

    if request.method == 'POST':
        username = session['username']

        return redirect(url_for('setting.update_profile'))

    salesman1, salesman2 = get_salesman()
    modual1, modual2 = get_modual()

    return render_template('setting_user/profile.html', current_time=current_time, user_name=user_name, user_level=user_level, one_name=one_name, two_name=two_name, three_name=three_name
                           ,rps_email=rps_email, rps_employee_id=rps_employee_id, rps_dpm=rps_dpm, rps_level=rps_level, rps_status=rps_status, salesman1=salesman1, salesman2=salesman2
                           ,modual1=modual1, modual2=modual2, rps_modual=rps_modual, photo_url=photo_url, user_moduals=user_moduals)

def get_salesman():
    salesman1 = ['SM001', 'SM002', 'SM003', 'SM004']
    salesman2 = ['SM001 | John Doe', 'SM002 | Jane Smith', 'SM003 | Mike Johnson', 'SM004 | Emily Davis']

    return salesman1, salesman2

def get_modual():
    modual1 = ['MD001', 'MD002', 'MD003', 'MD004']
    modual2 = ['Sales Module', 'Inventory Module', 'HR Module', 'Finance Module']

    return modual1, modual2

def upload_profile_picture():
    print(request.files)
    photo = request.files.get('upload')
    username = session['username']

    if photo:
        filename = f"{username}_{secure_filename(photo.filename)}"
        
        upload_folder = os.path.join(app.root_path, 'static', 'picture')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        image = Image.open(photo)
        image = image.resize((225, 224))

        image.save(os.path.join(upload_folder, filename))

        connection = connect_aep_portal()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE rps_tb_login 
            SET rps_photo = %s 
            WHERE rps_login_user = %s
        """, (filename, username))
        connection.commit()
        connection.close()

        print(f"File saved to: {os.path.join(upload_folder, filename)}")

        return redirect(url_for('setting.update_profile'))
    
    return 'No photo uploaded', 400