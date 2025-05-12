from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.pivot.summary_cus import get_salesman, get_selected_salesman_info
from backend.main_funtion import get_profile_picture_url
import random

def summary_type():
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
        summary, total_sum = summary_ty(selected_salesman, start_date, end_date, user_ids) 
    else:
        start_date = None
        end_date = None
        summary, total_sum = summary_ty(selected_salesman, start_date, end_date, user_ids) 
  
    selected_salesman_info = get_selected_salesman_info(selected_salesman)
    salesman1, salesman2 = get_salesman(user_ids, user_level)
    photo_url = get_profile_picture_url()

    return render_template('pivot/summary_type.html', salesman1=salesman1, salesman2=salesman2, photo_url=photo_url, user_moduals=user_moduals
                           ,selected_salesman_info=selected_salesman_info, selected_year=selected_year, total_sum=total_sum
                           , current_time=current_time, user_level=user_level, user_name=user_name, selected_sm=selected_sm, summary=summary)

def summary_ty(selected_salesman, start_date, end_date, user_ids):
    fake_data = []

    cust_types = ['กลุ่ม สายการบิน', 'กลุ่ม ร้านเบเกอรี่', 'กลุ่ม บริษัทฯ', 'กลุ่ม โรงงาน', 'กลุ่ม โรงแรม', 
                  'กลุ่ม บุคคลทั่วไป', 'กลุ่ม ร้านอาหาร-ยุโรป', 'กลุ่ม ร้านอาหาร-ฝรั่งเศส', 'กลุ่ม ร้านอาหาร-อิตาเลี่ยน', 
                  'กลุ่ม ร้านอาหาร-ญี่ปุ่น', 'กลุ่ม ร้านอาหาร-ไทย', 'กลุ่ม ร้านอาหาร-อิสลาม', 'กลุ่ม ร้านอาหาร-ทั่วไป', 
                  'กลุ่ม ร้านค้าส่ง', 'กลุ่ม ห้างสรรพสินค้า', 'อื่นๆ']

    for i in range(10):
        cust_type = cust_types[i % len(cust_types)]
        monthly_sales = [round(random.uniform(5000, 15000), 2) for _ in range(12)]
        total = sum(monthly_sales)

        fake_data.append([cust_type] + monthly_sales + [total])

    total_sum = sum(row[-1] for row in fake_data)

    return fake_data, total_sum