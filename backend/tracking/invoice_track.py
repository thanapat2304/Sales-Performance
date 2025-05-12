from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime, timedelta
from backend.main_funtion import get_profile_picture_url
import random

def invoice_track():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_id = session.get('user_group')
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    month_dict = {
    '01': 'มกราคม', '02': 'กุมภาพันธ์', '03': 'มีนาคม', '04': 'เมษายน',
    '05': 'พฤษภาคม', '06': 'มิถุนายน', '07': 'กรกฎาคม', '08': 'สิงหาคม',
    '09': 'กันยายน', '10': 'ตุลาคม', '11': 'พฤศจิกายน', '12': 'ธันวาคม'
    }

    if user_id and ',' in user_id:
        user_ids = tuple(user_id.split(','))
    else:
        user_ids = (user_id,)

    results = None
    growth_results = None
    selected_salesman = None
    selected_custno = None
    selected_customer = None
    selected_salesman_info = None
    selected_customer_info = None
    year_customer = None
    selected_sm = None
    selected_year = None
    selected_month = None
    date_track = None

    if request.method == 'POST':
        month_year = request.form['month_year']
        selected_year, selected_month = month_year.split('-') 
        selected_salesman = request.form['salesman']
        selected_custno = request.form['customer']
        selected_sm = request.form.get('salesman')
        selected_customer = request.form.get('customer')
        year_customer = request.form.get('year')
        date_track = request.form.get('month_year')

        results = execute_report_query(selected_salesman, selected_custno, selected_year, selected_month, user_ids)
        growth_results = fetch_growth_analysis(selected_salesman, selected_custno, selected_year, selected_month, user_ids)
        selected_customer_info = get_selected_customer_info(selected_custno)
        selected_salesman_info = get_selected_salesman_info(selected_salesman)

    salesman1, salesman2 = get_salesman(user_ids, user_level)
    customers1, customers2 = get_customers(user_ids)
    year = get_years()
    photo_url = get_profile_picture_url()

    selected_month_name = month_dict.get(selected_month, "ไม่ทราบเดือน")

    return render_template('tracking/invoice_track.html', customers1=customers1, customers2=customers2, salesman1=salesman1, salesman2=salesman2, year=year, results=results, growth_results=growth_results
                           ,selected_salesman_info=selected_salesman_info, selected_customer_info=selected_customer_info, selected_customer=selected_customer, selected_month=selected_month
                           ,year_customer=year_customer, current_time=current_time, user_level=user_level, user_name=user_name, selected_sm=selected_sm, selected_year=selected_year, date_track=date_track
                           ,selected_month_name=selected_month_name, photo_url=photo_url, user_moduals=user_moduals)

def get_salesman(user_ids, user_level):
    salesman1 = [f"SM{str(i+1).zfill(3)}" for i in range(10)]
    salesman2 = [f"{sm} | Salesman {i+1}" for i, sm in enumerate(salesman1)]

    salesman1.insert(0, "ALL")
    salesman2.insert(0, "ALL | ผู้ขายทั้งหมด")

    return salesman1, salesman2

def get_customers(user_ids):
    customers = [
        {"CUSTNO": 1001, "CUSTNAME": "Customer A"},
        {"CUSTNO": 1002, "CUSTNAME": "Customer B"},
        {"CUSTNO": 1003, "CUSTNAME": "Customer C"},
        {"CUSTNO": 1004, "CUSTNAME": "Customer D"},
        {"CUSTNO": 1005, "CUSTNAME": "Customer E"}
    ]
    
    customers1 = [str(customer["CUSTNO"]) for customer in customers]
    customers2 = [f"{customer['CUSTNO']} | {customer['CUSTNAME']}" for customer in customers]

    customers1.insert(0, "ALL")
    customers2.insert(0, "ALL | ลูกค้าทั้งหมด")

    return customers1, customers2

def get_years():
    current_year = datetime.now().year
    start_year = current_year - 3
    years = [{'id': str(year), 'AS_Name_year': str(year)} for year in range(current_year, start_year - 1, -1)]
    return years

def get_selected_customer_info(selected_custno):
    mock_customer_names = [
        "บริษัท สมาร์ทซัพพลาย จำกัด",
        "หจก. อิเล็กทรอนิกส์มาร์ท",
        "บจก. พีเอ็นเทคโนโลยี",
        "บริษัท เอ็นเตอร์ไพรส์ โกลบอล",
        "บจก. เคมีภัณฑ์ไทย"
    ]

    random_name = random.choice(mock_customer_names)
    return f"{selected_custno} | {random_name}"

def get_selected_salesman_info(selected_salesman):
    mock_salesman_names = [
        "ธนภัทร โสภณ",
        "วรินทร สมมติ",
        "ณัฐพงศ์ มั่วมา",
        "ศิริพร ตั้งเอา",
        "ปิยะดา มโน"
    ]

    random_name = random.choice(mock_salesman_names)
    return f"{selected_salesman} | {random_name}"

def all_customers(user_ids):
    mock_customer_prefixes = ["CUST", "CU", "CT", "CS"]
    num_customers = 10

    allcustomers = []
    for _ in range(num_customers):
        prefix = random.choice(mock_customer_prefixes)
        customer_code = f"{prefix}{random.randint(1000, 9999)}"
        allcustomers.append(customer_code)

    return list(set(allcustomers))

def fetch_growth_analysis(selected_salesman, selected_custno, selected_year, selected_month, user_ids):
    results = []
    base_date = datetime(int(selected_year), int(selected_month), 1)
    num_records = 10

    for _ in range(num_records):
        doc_date = base_date + timedelta(days=random.randint(0, 30))
        doc_no = f"DOC{random.randint(1000, 9999)}"
        cust_type = random.choice(['Retail', 'Wholesale'])
        cust_no = random.choice([f"CUST{random.randint(100, 999)}", selected_custno])
        cust_name = f"Customer {random.randint(1, 100)}"
        salesman = f"SM{random.randint(1, 5)}"
        total_bill = random.randint(1000, 10000)

        results.append((
            doc_date,
            doc_no,
            cust_type,
            cust_no,
            cust_name,
            f"{salesman} | SMName{random.randint(1, 10)}",
            float(total_bill)
        ))

    return results

def execute_report_query(selected_salesman, selected_custno, selected_year, selected_month, user_ids):
    results = []
    num_records = 10

    for _ in range(num_records):
        cust_type = random.choice(['Retail', 'Wholesale'])
        cust_no = f"CUST{random.randint(100, 999)}"
        cust_name = f"Customer {random.randint(1, 100)}"
        bill_day = random.randint(1, 31)
        total_bill = f"{random.randint(1, 10)} / {random.randint(1000, 10000)}"

        results.append((
            cust_type,
            cust_no,
            cust_name,
            bill_day,
            total_bill
        ))

    custno_data = {}

    month_days = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    selected_year_int = int(selected_year)
    if (selected_year_int % 4 == 0 and selected_year_int % 100 != 0) or (selected_year_int % 400 == 0):
        month_days[2] = 29

    for row in results:
        custype = row[0]
        custno = row[1]
        custname = row[2]
        bill_day = row[3]
        total_bill = row[4]

        if custno not in custno_data:
            selected_month_int = int(selected_month)
            custno_data[custno] = {'custname': custname, 'custype': custype, 'bills': {day: 0 for day in range(1, month_days[selected_month_int] + 1)}}

        custno_data[custno]['bills'][bill_day] = total_bill

    for custno, data in custno_data.items():
        total_quantity = 0
        total_amount = 0
        for day in range(1, month_days[int(selected_month)] + 1):
            if data['bills'][day] != 0:
                quantity, amount = data['bills'][day].split(' / ')
                total_quantity += float(quantity)
                total_amount += float(amount.replace('฿', '').replace(',', ''))
        
        data['total_quantity'] = int(total_quantity)
        data['total_amount'] = total_amount

    sorted_custno_data = dict(sorted(custno_data.items(), key=lambda item: item[1]['total_amount'], reverse=True))

    return sorted_custno_data