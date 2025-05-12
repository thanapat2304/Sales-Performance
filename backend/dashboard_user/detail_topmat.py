from flask import render_template, session
from datetime import datetime, timedelta
from backend.db_connection import connect_aep_DB
from backend.main_funtion import get_profile_picture_url
import random

def product_detail(matno):
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    custname = f"Product {matno}"

    purchase_data1 = []
    for i in range(5):
        custno = f"Cust{i+1:04}"
        matname = f"Customer {i+1}"
        last_purchase_date = datetime.now() - timedelta(days=random.randint(1, 60))
        last_purchase_amount = round(random.uniform(1000, 10000), 2)
        purchase_data1.append((custno, matname, last_purchase_date, last_purchase_amount))

    purchase_data2 = []
    for i in range(3):
        custno = f"Cust{i+6:04}"
        matname = f"Old Customer {i+6}"
        last_purchase_date = datetime.now() - timedelta(days=random.randint(61, 365))
        last_purchase_amount = round(random.uniform(500, 8000), 2)
        purchase_data2.append((custno, matname, last_purchase_date, last_purchase_amount))

    photo_url = get_profile_picture_url()
    
    return render_template(
        'dashboard_user/detail_topmat.html', 
        purchase_data1=purchase_data1,
        purchase_data2=purchase_data2,
        current_time=current_time,
        matno=matno,
        custname=custname,
        user_name=user_name,
        user_level=user_level,
        photo_url=photo_url
    )