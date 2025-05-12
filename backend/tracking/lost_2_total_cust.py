from flask import render_template, request
from backend.db_connection import connect_aep_DB
from backend.main_funtion import get_profile_picture_url
import random

def totallost2():
    selected_year = int(request.args.get('year'))
    selected_month = int(request.args.get('month'))
    
    data = query_customers(selected_year, selected_month)
    photo_url = get_profile_picture_url()

    return render_template('tracking/lost_2_total_cust.html', data=data, year=selected_year, month=selected_month, photo_url=photo_url)

def query_customers(year, month):
    fake_customers = []
    num_customers = random.randint(5, 15)

    for i in range(num_customers):
        custno = f"CUST{random.randint(1000, 9999)}"
        custname = f"Customer {random.randint(1, 100)}"
        smcode = f"SM{random.randint(10, 99)}"
        name = f"Salesman {random.randint(1, 50)}"
        latest_netamount = round(random.uniform(10000, 1000000), 2)

        fake_customers.append({
            "CUSTNO": custno,
            "CUSTNAME": custname,
            "SMCODE": smcode,
            "NAME": name,
            "LATEST_NETAMOUNT": latest_netamount
        })

    fake_customers.sort(key=lambda x: x["LATEST_NETAMOUNT"], reverse=True)

    return fake_customers