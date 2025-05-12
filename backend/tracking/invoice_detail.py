from flask import render_template, request, session
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import random

def detail_query():
    sample_data = [
        {'DOCDATE': '2025-05-10', 'DOCNO': 'INV12345', 'CUSTYPE': 'Driver1', 'CUSTNO': 'CUST001', 'CUSTNAME': 'Company A', 'SALESMAN': 'SM001 | Salesman A', 'total_bill': 15000.00},
        {'DOCDATE': '2025-05-09', 'DOCNO': 'INV12346', 'CUSTYPE': 'Driver2', 'CUSTNO': 'CUST002', 'CUSTNAME': 'Company B', 'SALESMAN': 'SM002 | Salesman B', 'total_bill': 23000.00},
        {'DOCDATE': '2025-05-08', 'DOCNO': 'INV12347', 'CUSTYPE': 'Driver1', 'CUSTNO': 'CUST003', 'CUSTNAME': 'Company C', 'SALESMAN': 'SM001 | Salesman A', 'total_bill': 10000.00},
        {'DOCDATE': '2025-05-07', 'DOCNO': 'INV12348', 'CUSTYPE': 'Driver3', 'CUSTNO': 'CUST004', 'CUSTNAME': 'Company D', 'SALESMAN': 'SM003 | Salesman C', 'total_bill': 18000.00},
        {'DOCDATE': '2025-05-06', 'DOCNO': 'INV12349', 'CUSTYPE': 'Driver2', 'CUSTNO': 'CUST005', 'CUSTNAME': 'Company E', 'SALESMAN': 'SM002 | Salesman B', 'total_bill': 12000.00},
    ]

    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    user_name = "John Doe"
    user_level = "Admin"
    photo_url = get_profile_picture_url()
    
    results = random.sample(sample_data, 3)

    return render_template('tracking/invoice_detail.html', results=results, user_name=user_name, user_level=user_level, current_time=current_time, photo_url=photo_url)