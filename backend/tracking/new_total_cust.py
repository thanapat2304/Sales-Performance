from flask import render_template, request
from backend.db_connection import connect_aep_DB
from backend.main_funtion import get_profile_picture_url
import random

def totalnew():
    selected_year = int(request.args.get('year'))
    selected_month = int(request.args.get('month'))
    
    data = query_customers(selected_year, selected_month)
    photo_url = get_profile_picture_url()

    return render_template('tracking/new_total_cust.html', data=data, year=selected_year, month=selected_month, photo_url=photo_url)

def query_customers(selected_year, selected_month):
    # สร้าง mock data แทนการดึงจากฐานข้อมูล
    customers = []
    num_records = random.randint(5, 15)  # สุ่มจำนวนลูกค้า

    for i in range(num_records):
        custno = f"CUST{random.randint(1000, 9999)}"
        custname = f"Customer {random.choice(['A', 'B', 'C', 'D', 'E'])}{i}"
        smcode = f"SM{random.randint(10, 99)}"
        smname = f"Salesman {random.choice(['X', 'Y', 'Z'])}{i}"
        latest_netamount = round(random.uniform(10000, 1000000), 2)

        customers.append({
            'CUSTNO': custno,
            'CUSTNAME': custname,
            'SMCODE': smcode,
            'NAME': smname,
            'LATEST_NETAMOUNT': latest_netamount
        })

    # จำลองการ sort ตาม LATEST_NETAMOUNT แบบเดียวกับ ORDER BY ใน SQL
    customers.sort(key=lambda x: x['LATEST_NETAMOUNT'], reverse=True)

    return customers