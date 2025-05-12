from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.tracking.invoice_track import get_salesman, get_customers, all_customers
from backend.main_funtion import get_profile_picture_url
import random

def customer_master():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_id = session.get('user_group')
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    if user_id and ',' in user_id:
        user_ids = tuple(user_id.split(','))
    else:
        user_ids = (user_id,)

    results = None
    selected_sm = None
    selected_salesman = None
    selected_custno = None
    selected_customer = None

    if request.method == 'POST':
        selected_salesman = request.form['salesman']
        selected_custno = request.form['customer']
        selected_sm = request.form.get('salesman')
        selected_customer = request.form.get('customer')

        results = master_cust(selected_salesman, selected_custno, user_ids)

    salesman1, salesman2 = get_salesman(user_ids, user_level)
    customers1, customers2 = get_customers(user_ids)
    photo_url = get_profile_picture_url()

    return render_template('main/cust_ms.html', customers1=customers1, customers2=customers2, salesman1=salesman1, salesman2=salesman2, user_name=user_name, current_time=current_time
                           ,selected_sm=selected_sm, selected_customer=selected_customer, results=results, user_level=user_level, photo_url=photo_url, user_moduals=user_moduals)

def master_cust(selected_salesman, selected_custno, user_ids):
    shop_types = ['Restaurant', 'Airline', 'Bakery', 'Company', 'Factory', 'Hotel', 'Individual', 'Other', 'WholeSale', 'Shopping Mall']

    customers = [
        {"CUSTNO": f"CUST{random.randint(1000, 9999)}", "CUSTNAME": f"Customer {random.randint(1, 100)}", "CUSTNAME_ENG": f"Customer {random.randint(1, 100)} ENG",
         "ADDRESS": f"Address {random.randint(1, 100)}", "TEL": f"0{random.randint(100000000, 999999999)}", "FAX": f"0{random.randint(100000000, 999999999)}", 
         "EMAIL": f"customer{random.randint(1, 100)}@example.com", "CONTPERS": f"Contact {random.randint(1, 100)}", "TAXID": f"1234567890", 
         "SMCODE": f"SM{random.randint(1, 10)}", "LINE_SHIP": f"Line {random.randint(1, 10)}"}
        for _ in range(10)
    ]
    
    for customer in customers:
        customer["SHOP TYPE"] = random.choice(shop_types)

    results = []
    for customer in customers:
        results.append((
            customer["SHOP TYPE"],
            customer["CUSTNO"],
            customer["CUSTNAME"],
            customer["CUSTNAME_ENG"],
            customer["ADDRESS"],
            customer["TEL"],
            customer["FAX"],
            customer["EMAIL"],
            customer["CONTPERS"],
            customer["TAXID"],
            customer["SMCODE"],
            f"Salesman {random.randint(1, 10)}",
            customer["LINE_SHIP"]
        ))

    return results