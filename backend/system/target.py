from flask import render_template, session
from backend.db_connection import connect_aep_portal
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import random

def target_sale():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    listbill = list_target()
    photo_url = get_profile_picture_url()
    count_sales, sum_sales, bkk_sales, rg_sales = Total_Target()

    return render_template('system/target.html', user_name=user_name, user_level=user_level, current_time=current_time, listbill=listbill, photo_url=photo_url, count_sales=count_sales
                           ,sum_sales=sum_sales, bkk_sales=bkk_sales, rg_sales=rg_sales, user_moduals=user_moduals)

def Total_Target():
    try:
        count_sales = random.randint(50, 200)
        sum_sales = random.randint(5_000_000, 20_000_000)
        bkk_sales = random.randint(2_000_000, sum_sales // 2)
        rg_sales = sum_sales - bkk_sales

        count_sales_str = f"{count_sales:,.0f}"
        sum_sales_str = f"฿ {sum_sales:,.0f}"
        bkk_sales_str = f"฿ {bkk_sales:,.0f}"
        rg_sales_str = f"฿ {rg_sales:,.0f}"

        return count_sales_str, sum_sales_str, bkk_sales_str, rg_sales_str
    except Exception as e:
        print(f"Error generating mock data: {e}")
        return "0", "฿ 0", "฿ 0", "฿ 0"

def list_target():
    mock_data = []
    num_rows = random.randint(5, 15)

    for i in range(num_rows):
        target_id = i + 1
        target_name = f"Sale {target_id}"

        monthly_targets = [random.randint(100_000, 500_000) for _ in range(12)]

        total_target = sum(monthly_targets)

        formatted_months = ["{:,.0f}".format(val) for val in monthly_targets]
        formatted_total = "{:,.0f}".format(total_target)

        mock_row = [target_id, target_name] + formatted_months + [formatted_total]
        mock_data.append(mock_row)

    return mock_data