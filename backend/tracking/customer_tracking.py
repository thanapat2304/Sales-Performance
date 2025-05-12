from flask import render_template, session, request, jsonify
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import random

def customer_track():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_id = session.get('user_group')
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    if user_id and ',' in user_id:
        user_ids = tuple(user_id.split(','))
    else:
        user_ids = (user_id,)

    summary = None
    results = None
    growth_results = None
    selected_salesman = None
    selected_custno = None
    selected_customer = None
    selected_year = None
    selected_salesman_info = None
    selected_customer_info = None
    year_customer = None
    selected_sm = None

    if request.method == 'POST':
        selected_salesman = request.form['salesman']
        selected_custno = request.form['customer']
        selected_year = request.form['year']
        selected_sm = request.form.get('salesman')
        selected_customer = request.form.get('customer')
        year_customer = request.form.get('year')
        results = execute_report_query(selected_salesman, selected_custno, selected_year, user_ids)
        growth_results = fetch_growth_analysis(selected_salesman, selected_custno, selected_year, user_ids)
        selected_customer_info = get_selected_customer_info(selected_custno)
        selected_salesman_info = get_selected_salesman_info(selected_salesman)
        summary = summary_cus(selected_salesman, selected_custno, selected_year, user_ids)

    salesman1, salesman2 = get_salesman(user_ids, user_level)
    customers1, customers2 = get_customers(user_ids)
    year = get_years()
    photo_url = get_profile_picture_url()

    return render_template('tracking/customer_tracking.html', customers1=customers1, customers2=customers2, salesman1=salesman1, salesman2=salesman2, year=year, results=results, growth_results=growth_results
                           ,selected_salesman_info=selected_salesman_info, selected_customer_info=selected_customer_info, selected_year=selected_year, selected_customer=selected_customer
                           ,year_customer=year_customer, current_time=current_time, user_level=user_level, user_name=user_name, selected_sm=selected_sm, summary=summary, photo_url=photo_url
                           ,user_moduals=user_moduals)

def get_salesman(user_ids, user_level):
    fake_salesmen = {
        user_id: f"{user_id} | Salesman {random.randint(1, 99)}"
        for user_id in user_ids
    }

    salesman1 = list(fake_salesmen.keys())
    salesman2 = list(fake_salesmen.values())

    if user_level in [1, 2]:
        salesman1.insert(0, "ALL")
        salesman2.insert(0, "ALL | ผู้ขายทั้งหมด")

    return salesman1, salesman2

def get_customers(user_ids):
    customers1 = []
    customers2 = []

    for _ in range(random.randint(5, 10)):
        custno = f"CUST{random.randint(1000, 9999)}"
        custname = f"ลูกค้า {random.choice(['สมชาย', 'สมศรี', 'วิทยา', 'จันทร์', 'พรทิพย์'])}"
        customers1.append(custno)
        customers2.append(f"{custno} | {custname}")

    customers1.insert(0, "ALL")
    customers2.insert(0, "ALL | ลูกค้าทั้งหมด")

    return customers1, customers2

def get_years():
    current_year = datetime.now().year
    start_year = current_year - 3
    years = [{'id': str(year), 'AS_Name_year': str(year)} for year in range(current_year, start_year - 1, -1)]
    return years

def get_selected_customer_info(selected_custno):
    customer_names = ['สมชาย', 'สมศรี', 'วิทยา', 'จันทร์', 'พรทิพย์']
    custname = random.choice(customer_names)
    
    full_customer = f"{selected_custno} | {custname}"
    
    return full_customer

def get_selected_salesman_info(selected_salesman):
    salesman_names = ['นายสมชาย', 'นางสาวสมศรี', 'คุณวิทยา', 'คุณจันทร์', 'คุณพรทิพย์']
    salesman_name = random.choice(salesman_names)
    
    full_salesman = f"{selected_salesman} | {salesman_name}"
    
    return full_salesman

def all_customers(user_ids):
    allcustomers = [f"CUST{random.randint(1000, 9999)}" for _ in range(10)]
    
    return allcustomers

def fetch_growth_analysis(selected_salesman, selected_custno, selected_year, user_ids):
    if not selected_year:
        return []

    selected_year = int(selected_year)
    one_year = selected_year - 1
    two_year = selected_year - 2
    three_year = selected_year - 3

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Total']
    results = []

    for month in months:
        amount_2022 = random.randint(10000, 500000)
        amount_2021 = random.randint(10000, 500000)
        amount_2023 = random.randint(10000, 500000)
        amount_2024 = random.randint(10000, 500000)

        def calculate_growth(current, previous):
            if previous == 0 and current == 0:
                return 0
            elif previous == 0:
                return 100
            else:
                return round((current - previous) / abs(previous) * 100, 2)

        growth_2021 = calculate_growth(amount_2022, amount_2021)
        growth_2022 = calculate_growth(amount_2023, amount_2022)
        growth_2023 = calculate_growth(amount_2024, amount_2023)

        row = (
            month,
            amount_2022,
            growth_2021,
            amount_2023,
            growth_2022,
            amount_2024,
            growth_2023
        )
        results.append(row)

    return results

def execute_report_query(selected_salesman, selected_custno, selected_year, user_ids):
    if not selected_year:
        return []

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    report_data = []

    for i in range(10):
        matno = f'MAT{i+1}'
        matdesc = f'Material {i+1}'
        brands = f'Brand {random.choice(["A", "B", "C"])}'
        uoms = f'UOM {random.choice(["kg", "ltr", "pcs"])}'

        monthly_data = []
        for month in range(12):
            qty = round(random.uniform(100, 500), 2)
            amount = round(random.uniform(1000, 5000), 2)
            monthly_data.append(f'{qty} / {amount}')
        
        total_qty = sum([round(random.uniform(100, 500), 2) for _ in range(12)])
        total_amount = sum([round(random.uniform(1000, 5000), 2) for _ in range(12)])
        monthly_data.append(f'{total_qty} / {total_amount}')

        report_data.append((
            matno, matdesc, brands, uoms, *monthly_data
        ))

    return report_data

def fetch_data():
    uoms = ['kg', 'ltr', 'pcs']
    last_purchase_dates = ['2024-01-01', '2024-02-01', '2024-03-01']

    prices = [round(random.uniform(100, 500), 2) for _ in range(3)]
    uom = random.choice(uoms)
    last_purchase_date = random.choice(last_purchase_dates)

    result = [{
        'UPRICE': price,
        'UOMs': uom,
        'LAST PURCHASE DATE': last_purchase_date
    } for price in prices]

    if result:
        prices = [row['UPRICE'] for row in result]
        uoms = [row['UOMs'] for row in result]
        last_purchase_dates = [row['LAST PURCHASE DATE'] for row in result]
        
        return jsonify({
            "price": prices,
            "uom": uoms,
            "last_purchase_date": last_purchase_dates
        })
    else:
        return jsonify({"error": "No data found"}), 404

def summary_cus(selected_salesman, selected_custno, selected_year, user_ids):
    customers = [
        {'CUSTNO': 'CUST001', 'CUSTNAME': 'Customer A'},
        {'CUSTNO': 'CUST002', 'CUSTNAME': 'Customer B'},
        {'CUSTNO': 'CUST003', 'CUSTNAME': 'Customer C'}
    ]

    def generate_sales_data():
        return {month: round(random.uniform(1000, 5000), 2) for month in range(1, 13)}

    result = []
    for customer in customers:
        sales_data = generate_sales_data()
        total_amount = sum(sales_data.values())
        result.append({
            'CUSTNO': customer['CUSTNO'],
            'CUSTNAME': customer['CUSTNAME'],
            'Jan': sales_data[1],
            'Feb': sales_data[2],
            'Mar': sales_data[3],
            'Apr': sales_data[4],
            'May': sales_data[5],
            'Jun': sales_data[6],
            'Jul': sales_data[7],
            'Aug': sales_data[8],
            'Sep': sales_data[9],
            'Oct': sales_data[10],
            'Nov': sales_data[11],
            'Dec': sales_data[12],
            'Total': total_amount
        })

    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No data found"}), 404