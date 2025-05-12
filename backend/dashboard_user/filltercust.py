from flask import render_template, request, session
from backend.db_connection import connect_aep_DB
from datetime import datetime, timedelta
import random

def show_results():
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    status = request.args.get('status', 'ALL')

    results = []
    for i in range(1, 21):
        total_sales = random.choice([0, random.randint(100000, 500000)])
        last_purchase_date = (datetime.now() - timedelta(days=random.randint(0, 400))).date() if total_sales > 0 else None
        customer_status = 'Active' if last_purchase_date and last_purchase_date >= datetime.now().date() - timedelta(days=365) else 'Non-Active'

        if status != 'ALL' and customer_status != status:
            continue

        results.append((
            f"CUST{i:04d} | Customer {i}",
            f"Customer ENG {i}",
            f"0{i}2-345-6789",
            f"SM{i:03d} | Sales {i}",
            f"{total_sales:,.2f}",
            last_purchase_date,
            customer_status
        ))

    return render_template('dashboard_user/fillter_cust.html', results=results, current_time=current_time)