from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.main_funtion import get_top, get_salesman, get_profile_picture_url
import random

def topcust():
    user_moduals = session.get('user_modual', '')
    english_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_month_number = datetime.now().month
    current_month = english_months[current_month_number - 1]
    month_one = english_months[current_month_number - 2]
    month_two = english_months[current_month_number - 3]
    current_year = datetime.now().year
    one_year = current_year - 1
    user_name = session.get('user_name', None)
    user_id = session.get('user_group')
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    if user_id and ',' in user_id:
        user_ids = tuple(user_id.split(','))
    else:
        user_ids = (user_id,)
    
    toptop = get_top()
    photo_url = get_profile_picture_url()
    salesman1, salesman2 = get_salesman(user_ids, user_level)

    results = None
    selected_salesman = None
    selected_top = None
    show_salesman = None
    show_top = None

    if request.method == 'POST':
        selected_salesman = request.form.get('salesman', 'ALL')
        selected_top = request.form.get('top', 10)
        show_salesman = request.form.get('salesman')
        show_top = request.form.get('top')
        results = data_top(selected_salesman, selected_top, user_ids)
    else:
        selected_salesman = 'ALL'
        selected_top = 10
        results = []

    sale_growth = []
    for row in results:
        if row[3] != 0:
            growth = ((row[2] - row[3]) / row[3] * 100)
            sale_growth.append(round(growth, 2))
        else:
            if row[2] > 0:
                sale_growth.append(100)
            elif row[2] == 0:
                sale_growth.append(0)
            else:
                sale_growth.append('N/A')

    return render_template('top_menu/top_cust.html', toptop=toptop, user_name=user_name, user_level=user_level, current_time=current_time, salesman1=salesman1, salesman2=salesman2,
                           photo_url=photo_url, results=results, sale_growth=sale_growth, current_month=current_month, month_one=month_one, month_two=month_two, current_year=current_year,
                           one_year=one_year, show_salesman=show_salesman, show_top=show_top, user_moduals=user_moduals)

def data_top(selected_salesman, selected_top, user_ids):
    selected_top = int(selected_top)

    results = []
    for i in range(selected_top):
        custno = f"CUST{i+1:04d}"
        custname = f"Customer {i+1}"
        total_now = random.randint(100000, 500000)
        total_one = random.randint(100000, 500000)
        sales_month_two = random.randint(10000, 50000)
        sales_month_one = random.randint(10000, 50000)
        sales_month_now = random.randint(10000, 50000)

        results.append((
            custno,
            custname,
            total_now,
            total_one,
            sales_month_two,
            sales_month_one,
            sales_month_now
        ))

    return results