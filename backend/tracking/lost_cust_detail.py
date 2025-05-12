from flask import render_template, session
from datetime import datetime, timedelta
from backend.db_connection import connect_aep_DB
from backend.main_funtion import get_profile_picture_url
import random

def lost_detail(custno):
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    custname = get_customer_name(custno)
    lost_list = lost_cust(custno)


    photo_url = get_profile_picture_url()

    return render_template('tracking/lost_cust_detail.html', current_time=current_time, lost_list=lost_list, custno=custno, custname=custname, user_name=user_name, user_level=user_level
                           ,photo_url=photo_url)

def lost_cust(custno):
    today = datetime.today()

    results = []

    for _ in range(10):
        matno = f"MAT{random.randint(1000, 9999)}"
        matname = f"Product {random.randint(1, 100)}"
        latest_purchase_date = today - timedelta(days=random.randint(0, 730))
        total_netamount = round(random.uniform(1000, 100000), 2)

        results.append((
            matno,
            matname,
            latest_purchase_date,
            total_netamount
        ))

    results.sort(key=lambda x: x[2], reverse=True)

    return results
    
def get_customer_name(custno):
    names = [
        "บริษัท สยามฟู้ด จำกัด", "ร้านค้าเจ๊แดง", "Customer Delight Co., Ltd.",
        "สมชาย มาร์เก็ต", "Happy Foods Group", "Quality Mart", 
        "Fresh Daily Co.", "Meena Minimart", "Top Value Store", "New Gen Foods"
    ]
    
    return random.choice(names)