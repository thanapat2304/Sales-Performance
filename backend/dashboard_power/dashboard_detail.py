from flask import render_template, session
from datetime import datetime
from backend.db_connection import connect_aep_DB, connect_aep_portal
from backend.dashboard_power.two_detail import fetch_Sum_Active, fetch_Sum_Cust, get_topic_data_sale
from decimal import Decimal
import random

def dash_detail(smcode):
    user_name = session.get('user_name', None)
    user_level = session.get('user_level', None)
    Monthly_target, Yearly_target = fetch_Sum_Target(smcode)
    Month_sales, NowYR_sales = Total_Actual(smcode)
    data = calculate_growth(smcode)
    customer = int(fetch_Sum_Cust(smcode))
    active_cust = int(fetch_Sum_Active(smcode))
    non_cust = customer - active_cust
    growth_data, total_target, total_actual = power_growth(smcode)
    donut = calculate_target(Monthly_target, Month_sales)
    sale_year = calculate_sales(Yearly_target, NowYR_sales)

    topic_data = get_topic_data_sale(smcode)
    topics = [row['End_Customer_Type'] for row in topic_data]
    counts = [row['total_customers_no_sales'] for row in topic_data]

    return render_template('dashboard_power/dashboard_detail.html', Monthly_target=Monthly_target, smcode=smcode, donut=donut, data=data, Month_sales=Month_sales
                           ,sale_year=sale_year, customer=customer, active_cust=active_cust, non_cust=non_cust, NowYR_sales=NowYR_sales
                           ,user_name=user_name, user_level=user_level, topics=topics, counts=counts, growth_data=growth_data, total_target=total_target, total_actual=total_actual
                           ,Yearly_target=Yearly_target)

def Total_Actual(smcode):
    Month_sales = Decimal(random.randint(200_000, 1_000_000))

    NowYR_sales = Decimal(random.randint(5_000_000, 20_000_000))

    return Month_sales, NowYR_sales

def fetch_Sum_Target(smcode):
    Monthly_target = Decimal(random.randint(1_000_000, 5_000_000))

    Yearly_target = Decimal(random.randint(10_000_000, 60_000_000))

    return Monthly_target, Yearly_target

def calculate_target(Monthly_target, Month_sales):
    if Monthly_target is None or Month_sales is None:
        return None

    try:
        target_value = float(str(Monthly_target).replace(",", ""))
        actual_value = float(str(Month_sales).replace(",", ""))

        if target_value > 0:
            percentage_of_target = (actual_value / target_value) * 100
            return round(percentage_of_target, 1)
        else:
            return None
    except ValueError:
        return None

def ytd_saleslate_report(smcode):
    current_year = datetime.now().year

    data = []
    for year in range(current_year - 3, current_year + 1):
        total_net_amount = Decimal(random.randint(3_000_000, 25_000_000))
        data.append({
            "year": year,
            "total_net_amount": total_net_amount
        })

    return data

def calculate_growth(smcode):
    english_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    ytd_late_data = ytd_saleslate_report(smcode)
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

def fetch_Sum_Year(smcode):
    total_Year = float(random.randint(10_000_000, 50_000_000))
    
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
    
def fetch_monthly_sale(smcode):
    monthly_values = {month: random.uniform(50000, 500000) for month in range(1, 13)}

    final_result = []
    
    for month in range(1, 13):
        value = monthly_values[month]
        final_result.append({
            'month': month,
            'total_asset_value': f"{value:,.2f}" if value != 0 else ''
        })

    return final_result
    
def fetch_monthly_one_sale(smcode):
    monthly_values = {month: random.uniform(50000, 500000) for month in range(1, 13)}

    final_result = []
    
    for month in range(1, 13):
        value = monthly_values[month]
        final_result.append({
            'month': month,
            'total_asset_value': f"{value:,.2f}" if value != 0 else ''
        })

    return final_result
    
def fetch_monthly_two_sale(smcode):
    monthly_values = {month: random.uniform(50000, 500000) for month in range(1, 13)}

    final_result = []
    
    for month in range(1, 13):
        value = monthly_values[month]
        final_result.append({
            'month': month,
            'total_asset_value': f"{value:,.2f}" if value != 0 else ''
        })

    return final_result
    
def sale_Sum_Target(smcode):
    try:
        mock_target_id = smcode
        mock_total_target = random.randint(10000, 100000)

        target_data = {mock_target_id: mock_total_target}
        return target_data
    except Exception as e:
        print(f"Error generating mock data: {e}")
        return {}

def sale_Sum_Actual(smcode):
    # สร้าง mock data โดยไม่ดึงข้อมูลจาก database
    fake_names = {
        'SM001': 'สมชาย ใจดี',
        'SM002': 'สมหญิง แสนดี',
        'SM003': 'อนันต์ ตั้งใจ',
        'SM004': 'สายใจ มั่นคง'
    }

    smname = fake_names.get(smcode, 'พนักงานไม่มีชื่อนี้')
    total_net_amount = round(random.uniform(100000, 500000), 2)

    actual_data = {
        smcode: {
            "SMNAME": smname,
            "total_net_amount": total_net_amount
        }
    }

    return actual_data

def power_growth(smcode):
    target_data = sale_Sum_Target(smcode)
    actual_data = sale_Sum_Actual(smcode)

    if not target_data or not actual_data:
        return {}, 0, 0, None

    growth_data = {}
    total_target = 0
    total_actual = 0

    for smcode, target in target_data.items():
        smcode_str = str(smcode)

        actual_info = actual_data.get(smcode_str, {"SMNAME": "Unknown", "total_net_amount": 0})
        actual = actual_info["total_net_amount"]
        smname = actual_info["SMNAME"]

        if target == 0:
            growth = None
        else:
            growth = ((actual - target) / target) * 100

        growth_data[smcode] = {
            "SMNAME": smname,
            "Target": target,
            "Actual": actual,
            "Growth (%)": growth if growth is not None else None
        }

    return growth_data, total_target, total_actual