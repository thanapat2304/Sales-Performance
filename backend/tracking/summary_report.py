from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.tracking.invoice_track import get_customers, all_customers
from backend.main_funtion import get_profile_picture_url
import random

def invoice_daily():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_id = session.get('user_group')
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    if user_id and ',' in user_id:
        user_ids = tuple(user_id.split(','))
    else:
        user_ids = (user_id,)

    bill_date = None
    results = None
    selected_salesman = None
    selected_sm = None
    selected_customer = None
    selected_cust = None

    if request.method == 'POST':
        selected_salesman = request.form['salesman']
        selected_customer = request.form['customer']
        bill_date = request.form['date']
        selected_sm = request.form.get('salesman')
        selected_cust = request.form.get('customer')

    if bill_date:
        start_date_str, end_date_str = bill_date.split(' - ')
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y').strftime('%Y/%m/%d')
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y').strftime('%Y/%m/%d')
    else:
        start_date = None
        end_date = None

    results = get_sales_data(selected_salesman, selected_customer, start_date, end_date, user_ids)
    salesman1, salesman2 = get_salesman(user_ids, user_level)
    customers1, customers2 = get_customers(user_ids)
    total_sales, total_vat = get_sales_total(selected_salesman, selected_customer, start_date, end_date, user_ids)

    total_sales_value = float(total_sales.replace(',', '').replace('฿', '').strip()) if total_sales else 0.0
    total_vat_value = float(total_vat.replace(',', '').replace('฿', '').strip()) if total_vat else 0.0

    total = total_sales_value + total_vat_value

    total_formatted = f"{total:,.2f}"
    photo_url = get_profile_picture_url()

    return render_template('tracking/summary_report.html', salesman1=salesman1, salesman2=salesman2, results=results, selected_sm=selected_sm, customers1=customers1, total_vat=total_vat
                           , current_time=current_time, user_level=user_level, user_name=user_name, customers2=customers2, selected_cust=selected_cust, total_sales=total_sales
                           , total_formatted=total_formatted, photo_url=photo_url, user_moduals=user_moduals)

def get_salesman(user_id, user_level):
    mock_salesman_codes = ['S001', 'S002', 'S003', 'S004', 'S005']
    mock_salesman_names = ['สมชาย', 'สมพร', 'สมบัติ', 'สมจิต', 'สมศักดิ์']

    salesman1 = random.sample(mock_salesman_codes, 3)
    salesman2 = [f"{code} | {random.choice(mock_salesman_names)}" for code in salesman1]

    if user_level in [1, 2]:
        salesman1.insert(0, "ALL")
        salesman2.insert(0, "ALL | ผู้ขายทั้งหมด")

    return salesman1, salesman2

def get_selected_salesman_info(selected_salesman):
    mock_salesman_data = {
        'S001': 'สมชาย',
        'S002': 'สมพร',
        'S003': 'สมบัติ',
        'S004': 'สมจิต',
        'S005': 'สมศักดิ์'
    }

    if selected_salesman in mock_salesman_data:
        full_salesman = f"{selected_salesman} | {mock_salesman_data[selected_salesman]}"
        return full_salesman
    else:
        return None

def get_sales_data(selected_salesman, selected_customer, start_date, end_date, user_ids):
    mock_data = [
        {
            'DT': 'TX',
            'DOC_NUMBER': str(random.randint(1000, 9999)),
            'DOCDATE': (datetime.now()).strftime('%d/%m/%Y'),
            'CUSTOMER': f"CUST{random.randint(100, 999)} | {random.choice(['ร้านอาหาร', 'โรงแรม', 'บริษัท'])}",
            'SHOP_TYPE': random.choice(['Restaurant', 'Airline', 'Hotel', 'Company']),
            'SHIPLINE': random.choice(['Line A', 'Line B', 'Line C']),
            'SALESMAN': f"S001 | สมชาย",
            'CREATE ORDER BY': random.choice(['User1', 'User2', 'User3'])
        }
        for _ in range(10)
    ]

    return mock_data

def get_sales_total(selected_salesman, selected_customer, start_date, end_date, user_ids):
    def fetch_total(column_name, note):
        mock_data = {
            'NETAMOUNT': random.uniform(10000, 50000),
            'VAT': random.uniform(1000, 5000)
        }

        total = mock_data.get(column_name, 0.00)

        formatted_total = f"{total:,.2f}"
        return formatted_total

    total_sales = fetch_total('NETAMOUNT', 'sale')
    total_vat = fetch_total('VAT', 'vat')

    return total_sales, total_vat