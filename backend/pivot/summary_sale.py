from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.pivot.summary_cus import get_selected_salesman_info
from backend.main_funtion import get_profile_picture_url, get_all_sales_target
import random

def summary_sale():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_id = session.get('user_group')
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    if user_id and ',' in user_id:
        user_ids = tuple(user_id.split(','))
    else:
        user_ids = (user_id,)

    summary = None
    total_sum = 0
    selected_salesman = None
    selected_year = None
    selected_salesman_info = None
    selected_sm = None
    bill_date = None

    if request.method == 'POST':
        selected_salesman = request.form['salesman']
        bill_date = request.form['date']
        selected_sm = request.form.get('salesman')

    if bill_date:
        start_date_str, end_date_str = bill_date.split(' - ')
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y').strftime('%Y/%m/%d')
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y').strftime('%Y/%m/%d')
    else:
        start_date = None
        end_date = None

    selected_salesman_info = get_selected_salesman_info(selected_salesman)
    summary, total_sum = summary_ty(selected_salesman, start_date, end_date, user_ids, user_level)
    salesman1, salesman2 = get_salesman(user_ids, user_level)
    photo_url = get_profile_picture_url()

    return render_template('pivot/summary_sale.html', salesman1=salesman1, salesman2=salesman2, photo_url=photo_url, user_moduals=user_moduals
                           ,selected_salesman_info=selected_salesman_info, selected_year=selected_year, total_sum=total_sum
                           , current_time=current_time, user_level=user_level, user_name=user_name, selected_sm=selected_sm, summary=summary)

def summary_ty(selected_salesman, start_date, end_date, user_ids, user_level):
    fake_data = []
    salesman_names = ['Salesman A', 'Salesman B', 'Salesman C', 'Salesman D', 'Salesman E']

    for i in range(10):
        smcode = f'SM{random.randint(1, 100)}'
        smname = random.choice(salesman_names)
        monthly_sales = [round(random.uniform(1000, 5000), 2) for _ in range(12)]
        total_sales = sum(monthly_sales)

        fake_data.append([smcode, smname] + monthly_sales + [total_sales])

    total_sum = sum(row[-1] for row in fake_data)

    return fake_data, total_sum

def get_salesman(user_ids, user_level):
    fake_salesmen = {
        user_id: f"{user_id} | Salesman {random.randint(1, 99)}"
        for user_id in user_ids
    }

    salesman1 = list(fake_salesmen.keys())
    salesman2 = list(fake_salesmen.values())

    if user_level in [1, 2]:
        salesman1.insert(0, "ALL")
        salesman2.insert(0, "ALL | ผู้ขายทั้งหมด")

    return salesman1, salesman2