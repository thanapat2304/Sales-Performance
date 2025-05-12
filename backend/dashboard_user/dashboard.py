from flask import render_template, session
from backend.db_connection import connect_aep_portal , connect_aep_DB
from datetime import datetime
from backend.dashboard_user.two_dashboard import fetch_Sum_Cust, fetch_Sum_Active, get_topic_data
from decimal import Decimal
import random

def dashboard_sale():
    user_moduals = session.get('user_modual', '')
    user_level = session.get('user_level', None)
    english_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    data = calculate_growth()
    customer = fetch_Sum_Cust()
    active_cust = fetch_Sum_Active()
    non_cust = customer - active_cust
    current_month_number = datetime.now().month
    current_month = english_months[current_month_number - 1]
    month_one = english_months[current_month_number - 2]
    month_two = english_months[current_month_number - 3]
    current_year = datetime.now().year
    one_year = current_year - 1
    two_year = current_year - 2
    Month_sales, NowYR_sales = Total_Actual()
    Monthly_target, Yearly_target = fetch_Sum_Target()
    donut = calculate_target(Monthly_target, Month_sales)
    sale_year = calculate_sales(Yearly_target, NowYR_sales)
    topic_data = get_topic_data()
    topics = [row['End_Customer_Type'] for row in topic_data]
    counts = [row['total_customers_no_sales'] for row in topic_data]

    return render_template('dashboard_user/dashboard_user.html', data=data, current_month_number=current_month_number, current_year=current_year, one_year=one_year, two_year=two_year
                           ,Monthly_target=Monthly_target, Month_sales=Month_sales, donut=donut, sale_year=sale_year, NowYR_sales=NowYR_sales, Yearly_target=Yearly_target
                           ,current_month=current_month, month_one=month_one, month_two=month_two, customer=customer, active_cust=active_cust, topics=topics, counts=counts
                           , user_level=user_level, non_cust=non_cust, user_moduals=user_moduals)

def Total_Actual():
    Month_sales = Decimal(random.randint(200_000, 1_000_000))

    NowYR_sales = Decimal(random.randint(5_000_000, 20_000_000))

    return Month_sales, NowYR_sales

def ytd_saleslate_report():
    current_year = datetime.now().year

    data = []
    for year in range(current_year - 3, current_year + 1):
        total_net_amount = Decimal(random.randint(3_000_000, 25_000_000))
        data.append({
            "year": year,
            "total_net_amount": total_net_amount
        })

    return data

def calculate_growth():
    english_months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    ytd_late_data = ytd_saleslate_report()
    current_day = datetime.now().day
    current_month = english_months[datetime.now().month - 1]
    current_year = datetime.now().year

    ytd_late_dict = {row["year"]: row["total_net_amount"] for row in ytd_late_data}

    target_years = [current_year - 2, current_year - 1, current_year]
    growth_data = []

    for year in target_years:
        current_total = ytd_late_dict.get(year, 0)
        previous_total = ytd_late_dict.get(year - 1, 0)

        growth_percentage = None
        if previous_total and previous_total > 0:
            growth_percentage = ((current_total - previous_total) / previous_total) * 100

        if current_total is None:
            current_total = 0

        growth_data.append({
            "year": year,
            "actual_sale": f"Actual sale 1 Jan - {current_day} {current_month}",
            "total_net_amount": f"{current_total:,.2f}",
            "growth_percentage": growth_percentage
        })

    return growth_data

def fetch_Sum_Target():
    Monthly_target = Decimal(random.randint(1_000_000, 5_000_000))

    Yearly_target = Decimal(random.randint(10_000_000, 60_000_000))

    return Monthly_target, Yearly_target

def fetch_Sum_Actual():
    total_Actual = float(random.randint(1_000_000, 5_000_000))
    return total_Actual

def calculate_target(Monthly_target, actual):

    if Monthly_target is None or actual is None:
        return None

    try:
        Monthly_target = str(Monthly_target)
        if "k" in Monthly_target:
            target_value = float(Monthly_target.replace(" k", "").replace(",", "")) * 1000
        else:
            target_value = float(Monthly_target.replace(",", ""))

        actual_value = float(actual)

        if target_value > 0:
            percentage_of_target = (actual_value / target_value) * 100
            return round(percentage_of_target, 1)
        else:
            return None
    except ValueError:
        return None
    
def fetch_Sum_Year():
    total_Year = float(random.randint(10_000_000, 50_000_000))
    
    formatted_Year = f"{total_Year:,.2f}"
    return formatted_Year

def fetch_Sum_Year_late():
    total_Year = float(random.randint(5_000_000, 30_000_000))
    
    formatted_Year = f"{total_Year:,.2f}"
    return formatted_Year

def calculate_sales(Yearly_target, NowYR_sales):
    if Yearly_target == 0:
        return None

    try:
        if isinstance(NowYR_sales, Decimal):
            NowYR_sales = float(NowYR_sales)
        else:
            NowYR_sales = float(str(NowYR_sales).replace(",", "")) if NowYR_sales else 0

        if isinstance(Yearly_target, Decimal):
            Yearly_target = float(Yearly_target)
        else:
            Yearly_target = float(str(Yearly_target).replace(",", "")) if Yearly_target else 0

        if Yearly_target > 0:
            percentage = (NowYR_sales / Yearly_target) * 100
            return round(percentage, 2)
        else:
            return None
    except ValueError:
        return None
    
def calculate_sales_percentage():
    sales_current_year = fetch_Sum_Year()
    sales_last_year = fetch_Sum_Year_late()

    try:
        sales_current_year = float(sales_current_year.replace(",", "")) if sales_current_year else 0
        sales_last_year = float(sales_last_year.replace(",", "")) if sales_last_year else 0
    except ValueError:
        return None

    if sales_last_year > 0:
        percentage_change = ((sales_current_year - sales_last_year) / sales_last_year) * 100
        return round(percentage_change, 1)
    else:
        return None

def fetch_monthly():
    monthly_values = {month: random.uniform(50000, 500000) for month in range(1, 13)}

    final_result = []
    
    for month in range(1, 13):
        value = monthly_values[month]
        final_result.append({
            'month': month,
            'total_asset_value': f"{value:,.2f}" if value != 0 else ''
        })

    return final_result
    
def fetch_monthly_one():
    monthly_values = {month: random.uniform(50000, 500000) for month in range(1, 13)}

    final_result = []
    
    for month in range(1, 13):
        value = monthly_values[month]
        final_result.append({
            'month': month,
            'total_asset_value': f"{value:,.2f}" if value != 0 else ''
        })

    return final_result
    
def fetch_monthly_two():
    monthly_values = {month: random.uniform(50000, 500000) for month in range(1, 13)}

    final_result = []
    
    for month in range(1, 13):
        value = monthly_values[month]
        final_result.append({
            'month': month,
            'total_asset_value': f"{value:,.2f}" if value != 0 else ''
        })

    return final_result