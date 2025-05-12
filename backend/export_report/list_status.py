from flask import render_template, session, send_file, request, redirect, url_for, jsonify
from backend.db_connection import connect_aep_DB, connect_aep_portal
from datetime import datetime
from backend.main_funtion import get_profile_picture_url, get_salesman_all
import random

def status_list():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    listsales = list_sales()
    photo_url = get_profile_picture_url()

    active1_sales, active2_sales, active3_sales, non_active = Total_status()

    salesman1,salesman2 = get_salesman_all()

    status_data = get_status()

    if request.method == 'POST':
        data = request.get_json()

        name_sales = data.get('sales')
        name_nick_name = data.get('nick_name')
        name_status = data.get('status')

        sales_id, full_name = name_sales.split(' | ')

        return jsonify({'message': 'Data successfully added!'}), 200

    return render_template('export_report/list_status.html', user_name=user_name, user_level=user_level, current_time=current_time, photo_url=photo_url, user_moduals=user_moduals,
                           listsales=listsales, active1_sales=active1_sales, active2_sales=active2_sales, active3_sales=active3_sales, non_active=non_active, salesman2=salesman2, status_data=status_data)

def get_status():
    return [
        "1 Active",
        "2 Active (Region)",
        "3 Active (Offline)",
        "Non Active"
    ]

def list_sales():
    remarks = ['1 Active', '2 Active (Region)', '3 Active (Offline)', 'Non Active']
    regions = ['thapurt', 'mask elon', 'East West', 'West korea', 'South linne']
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Hannah']

    mock_results = []
    for i in range(20):
        smcode = f"SM{1000 + i}"
        smname = random.choice(names)
        region = random.choice(regions)
        remark = random.choice(remarks)

        row = (smcode, smname, region, remark)
        mock_results.append(row)

    mock_results.sort(key=lambda x: x[3])

    return mock_results

def Total_status():
    try:
        active1_sales = f"{random.randint(50, 200):,}"
        active2_sales = f"{random.randint(30, 150):,}"
        active3_sales = f"{random.randint(10, 100):,}"
        non_active = f"{random.randint(0, 80):,}"

        return active1_sales, active2_sales, active3_sales, non_active
    except Exception as e:
        print(f"Error generating mock data: {e}")
        return "0", "0", "0", "0"