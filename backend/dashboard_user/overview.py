from flask import render_template, session
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import random
from collections import defaultdict

def sales_overview():
    user_moduals = session.get('user_modual', '')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    user_level = session.get('user_level')
    user_name = session.get('user_name', None)

    sorted_data = get_sales_data()

    photo_url = get_profile_picture_url()

    return render_template('dashboard_user/overview_user.html', sorted_data=sorted_data, current_time=current_time, photo_url=photo_url, user_level=user_level, user_name=user_name
                           ,user_moduals=user_moduals)


def get_sales_data():
    data = defaultdict(lambda: [0] * 12)

    for year in range(2023, 2026):
        for month in range(1, 13):
            total_sales = random.randint(100000, 500000)
            data[year][month - 1] = total_sales

    for year in data:
        total_year_sales = sum(data[year])
        data[year].append(total_year_sales)

    sorted_data = sorted(data.items(), reverse=True)

    return sorted_data

def fetch_monthly_over():
    monthly_values = {i: 0.00 for i in range(1, 13)}

    for month in range(1, 13):
        total_sales = random.uniform(100000.0, 500000.0)
        monthly_values[month] = total_sales

    final_result = []
    for month in range(1, 13):
        value = monthly_values[month]
        final_result.append({
            'month': month,
            'total_asset_value': f"{value:.2f}"
        })

    return final_result
    
def fetch_monthly_one_over():
    monthly_values = {i: 0.00 for i in range(1, 13)}

    for month in range(1, 13):
        total_sales = random.uniform(100000.0, 500000.0)
        monthly_values[month] = total_sales

    final_result = []
    for month in range(1, 13):
        value = monthly_values[month]
        final_result.append({
            'month': month,
            'total_asset_value': f"{value:.2f}"
        })

    return final_result
    
def fetch_monthly_two_over():
    monthly_values = {i: 0.00 for i in range(1, 13)}

    for month in range(1, 13):
        total_sales = random.uniform(100000.0, 500000.0)
        monthly_values[month] = total_sales

    final_result = []
    for month in range(1, 13):
        value = monthly_values[month]
        final_result.append({
            'month': month,
            'total_asset_value': f"{value:.2f}"
        })

    return final_result