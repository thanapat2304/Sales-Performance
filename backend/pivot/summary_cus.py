from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import random

def summary_customer():
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
        selected_customer_info = get_selected_customer_info(selected_custno)
        selected_salesman_info = get_selected_salesman_info(selected_salesman)
        summary = summary_cus(selected_salesman, selected_custno, selected_year, user_ids)

    salesman1, salesman2 = get_salesman(user_ids, user_level)
    customers1, customers2 = get_customers(user_ids)
    year = get_years()
    photo_url = get_profile_picture_url()

    return render_template('pivot/summary_cus.html', customers1=customers1, customers2=customers2, salesman1=salesman1, salesman2=salesman2, year=year, photo_url=photo_url, user_moduals=user_moduals
                           ,selected_salesman_info=selected_salesman_info, selected_customer_info=selected_customer_info, selected_year=selected_year, selected_customer=selected_customer
                           ,year_customer=year_customer, current_time=current_time, user_level=user_level, user_name=user_name, selected_sm=selected_sm, summary=summary)

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

def summary_cus(selected_salesman, selected_custno, selected_year, user_ids):

    fake_data = []

    cust_types = ['กลุ่ม สายการบิน', 'กลุ่ม ร้านเบเกอรี่', 'กลุ่ม บริษัทฯ', 'กลุ่ม โรงงาน', 'กลุ่ม โรงแรม', 
                  'กลุ่ม บุคคลทั่วไป', 'กลุ่ม ร้านอาหาร-ยุโรป', 'กลุ่ม ร้านอาหาร-ฝรั่งเศส', 'กลุ่ม ร้านอาหาร-อิตาเลี่ยน', 
                  'กลุ่ม ร้านอาหาร-ญี่ปุ่น', 'กลุ่ม ร้านอาหาร-ไทย', 'กลุ่ม ร้านอาหาร-อิสลาม', 'กลุ่ม ร้านอาหาร-ทั่วไป', 
                  'กลุ่ม ร้านค้าส่ง', 'กลุ่ม ห้างสรรพสินค้า', 'อื่นๆ']
    
    for i in range(10):
        custno = f"CUST{1000 + i}"
        custname = f"Customer {i+1}"
        cust_type = cust_types[i % len(cust_types)]
        monthly_sales = [round(random.uniform(1000, 10000), 2) for _ in range(12)]
        total = sum(monthly_sales)

        fake_data.append([custno, custname, cust_type] + monthly_sales + [total])

    return fake_data