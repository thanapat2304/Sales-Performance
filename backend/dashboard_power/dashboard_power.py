from flask import render_template, session
from backend.db_connection import connect_aep_portal , connect_aep_DB
from datetime import datetime
from backend.dashboard_user.dashboard import calculate_growth, calculate_target, Total_Actual, fetch_Sum_Target
import random

def dashboard_two():
    user_moduals = session.get('user_modual', '')
    user_level = session.get('user_level', None)
    english_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_month_number = datetime.now().month
    current_month = english_months[current_month_number - 1]
    month_one = english_months[current_month_number - 2]
    month_two = english_months[current_month_number - 3]
    data = calculate_growth()
    Month_sales, NowYR_sales = Total_Actual()
    Monthly_target, Yearly_target = fetch_Sum_Target()
    donut = calculate_target(Monthly_target, Month_sales)
    current_year = datetime.now().year
    one_year = current_year - 1
    two_year = current_year - 2
    target = sale_Sum_Target()
    actual_data = sale_Sum_Actual()
    if actual_data is None:
        print("Error: actual_data is None. Check sale_Sum_Actual().")
        actual_data = {}

    growth_data, total_target, total_actual, total_growth, total_null, growth_null = power_growth(actual_data, target)

    return render_template('dashboard_power/dashboard_power.html', growth_data=growth_data, total_target=total_target, total_actual=total_actual, total_growth=total_growth
                           , data=data, Monthly_target=Monthly_target, Month_sales=Month_sales, donut=donut, current_month=current_month, user_moduals=user_moduals
                           ,month_one=month_one, month_two=month_two, user_level=user_level, total_null=total_null, growth_null=growth_null, current_year=current_year
                           ,one_year=one_year, two_year=two_year)

def sale_Sum_Target():
    mock_user_ids = ['SM001', 'SM002', 'SM003', 'SM004', 'SM005']

    target_data = {}
    for uid in mock_user_ids:
        monthly_target = random.randint(200_000, 1_000_000)
        target_data[uid] = monthly_target

    return target_data

def get_rps_target_ids():
    mock_ids = [101, 102, 103, 104, 105]

    return ",".join(str(id) for id in mock_ids)

def sale_Sum_Actual():
    user_level = session.get('user_level', None)
    user_id = session.get('user_group', None)

    if user_level == 1:
        actual_data = {
            '101': {"SMNAME": "John Smith", "total_net_amount": 100000.00},
            '102': {"SMNAME": "Jane Doe", "total_net_amount": 95000.00},
            'NULL-SALES': {"SMNAME": "NULL-SALES", "total_net_amount": 12000.00}
        }
    else:
        actual_data = {
            '103': {"SMNAME": "Mike Johnson", "total_net_amount": 48000.50},
            '104': {"SMNAME": "Emily Davis", "total_net_amount": 30500.75}
        }

    return actual_data

def mock_target_1_data():
    return {
        '101': 90000,
        '102': 515841,
        '103': 80000,
        '104': 60000,
        '105': 0,
        '999': 120000
    }

def power_growth(actual_data, target_1_data):
    if not target_1_data or not actual_data:
        return {}, 0, 0, None

    growth_data = {}
    total_target = 0
    total_actual = 0
    total_null = 0

    rps_target_data_str = mock_target_1_data()

    for smcode, actual_info in actual_data.items():
        smcode_str = str(smcode)
        smname = actual_info["SMNAME"]
        actual = actual_info["total_net_amount"]

        target = rps_target_data_str.get(smcode_str, 0)

        if target == 0:
            growth = 0
        else:
            growth = (actual / target) * 100
            total_actual += actual

        growth_data[smcode] = {
            "SMNAME": smname,
            "Target": target,
            "Actual": actual,
            "Growth (%)": growth
        }

        total_target += target
        total_null += actual

    if total_target == 0:
        total_growth = None
    else:
         total_growth = (total_actual / total_target) * 100

    growth_null = (total_null / total_target) * 100

    return growth_data, total_target, total_actual, total_growth, total_null, growth_null