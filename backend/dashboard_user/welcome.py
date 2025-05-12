from flask import render_template, session
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import random

def welcome_sale():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    listbill = list_bill()
    daily, monthly ,yearly = Total_Actual()
    TX_sales, CN_sales ,DN_sales = Total_txcddn()
    TX = Sum_TX()
    photo_url = get_profile_picture_url()

    return render_template('dashboard_user/welcome.html', user_name=user_name, user_level=user_level, current_time=current_time, daily=daily, monthly=monthly, yearly=yearly, listbill=listbill
                           , TX=TX, TX_sales=TX_sales, CN_sales=CN_sales, DN_sales=DN_sales, photo_url=photo_url, user_moduals=user_moduals)

def Sum_TX():

    total_Actual = random.randint(0, 1000)

    formatted_Actual = f"{total_Actual:,}"
    
    return formatted_Actual


def Total_Actual():
    daily_sales_value = random.randint(10_000, 500_000)
    monthly_sales_value = random.randint(500_000, 5_000_000)
    yearly_sales_value = random.randint(5_000_000, 60_000_000)

    daily_sales = f"฿ {daily_sales_value:,.0f}"
    monthly_sales = f"฿ {monthly_sales_value:,.0f}"
    yearly_sales = f"฿ {yearly_sales_value:,.0f}"

    return daily_sales, monthly_sales, yearly_sales

def list_bill():
    num_records = random.randint(5, 15)

    shop_types = ['Restaurant', 'Airline', 'Bakery', 'Company', 'Factory', 'Hotel', 'Individual', 'Other', 'WholeSale', 'Shopping Mall']
    salesman_names = ['SM001 | John Doe', 'SM002 | Jane Smith', 'SM003 | Alice Johnson', 'SM004 | Bob Lee']
    create_order_users = ['admin', 'user1', 'user2', 'operator']
    shipline_name = ['สำนักงานใหญ่', 'สาขาศรีราชา', 'สาขาอุดร', 'สาขาโคราช']

    today = datetime.now().strftime("%d/%m/%Y")

    results = []

    for i in range(num_records):
        dt = 'TX'
        doc_number = f"{random.randint(100000000, 999999999)}"
        docdate = today
        customer = f"CUST{random.randint(1000, 9999)} | บริษัทตัวอย่าง {random.randint(1, 99)}"
        shop_type = random.choice(shop_types)
        shipline = random.choice(shipline_name)
        salesman = random.choice(salesman_names)
        created_by = random.choice(create_order_users)

        record = (dt, doc_number, docdate, customer, shop_type, shipline, salesman, created_by)
        results.append(record)

    return results

def Total_txcddn():
    user_id = session.get('user_group', None)

    tx_sales_value = random.randint(100_000, 5_000_000)
    cn_sales_value = random.randint(10_000, 500_000)
    dn_sales_value = random.randint(5_000, 300_000)

    tx_sales = f"฿ {tx_sales_value:,.0f}"
    cn_sales = f"฿ {cn_sales_value:,.0f}"
    dn_sales = f"฿ {dn_sales_value:,.0f}"

    return tx_sales, cn_sales, dn_sales