from flask import render_template, session
from backend.db_connection import connect_aep_DB
from datetime import datetime, timedelta
from backend.main_funtion import get_profile_picture_url
import random

def lost_sale():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    two_months_results, six_months_results, one_year_results = lostcust_two()
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    photo_url = get_profile_picture_url()

    return render_template('tracking/lost_cust.html', two_months_results=two_months_results, current_time=current_time, user_name=user_name, user_level=user_level
                           ,six_months_results=six_months_results, one_year_results=one_year_results, photo_url=photo_url, user_moduals=user_moduals)

def lostcust_two():
    today = datetime.today()
    two_months = today - timedelta(days=60)
    six_months = today - timedelta(days=180)
    one_year = today - timedelta(days=365)

    results = []

    for _ in range(20):
        custno = f"CUST{random.randint(1000, 9999)}"
        custname = f"Customer {random.randint(1, 100)}"
        latest_purchase_date = today - timedelta(days=random.randint(0, 730))
        net_amount = round(random.uniform(10000, 500000), 2)
        custype = random.choice(['Retail', 'Wholesale', 'Restaurant', 'Hotel'])

        results.append((
            custype,
            custno,
            custname,
            latest_purchase_date,
            net_amount
        ))

    two_months_results = []
    six_months_results = []
    one_year_results = []

    for row in results:
        docdate = row[3]
        if docdate < two_months:
            two_months_results.append(row)
        if docdate < six_months:
            six_months_results.append(row)
        if docdate < one_year:
            one_year_results.append(row)

    return two_months_results, six_months_results, one_year_results