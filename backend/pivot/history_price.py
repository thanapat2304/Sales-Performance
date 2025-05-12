from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.pivot.summary_cus import get_customers, all_customers
from backend.main.stock import get_product
from backend.main_funtion import get_profile_picture_url
import random

def history_price():
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
    total_sum = 0
    bill_date = None
    selected_product = None
    selected_custno = None
    selected_mat = None
    selected_customer = None

    if request.method == 'POST':
        selected_product = request.form['product']
        selected_custno = request.form['customer']
        bill_date = request.form['date']
        selected_mat = request.form.get('product')
        selected_customer = request.form.get('customer')

    if bill_date:
        start_date_str, end_date_str = bill_date.split(' - ')
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y').strftime('%Y/%m/%d')
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y').strftime('%Y/%m/%d')
    else:
        start_date = None
        end_date = None

    summary, total_sum = summary_ty(selected_product, selected_custno, start_date, end_date, user_ids)
    customers1, customers2 = get_customers(user_ids)
    product1, product2 = get_product()
    photo_url = get_profile_picture_url()

    return render_template('pivot/history_price.html', customers1=customers1, customers2=customers2, product2=product2, photo_url=photo_url, user_moduals=user_moduals
                           , total_sum=total_sum, product1=product1, selected_mat=selected_mat, selected_customer=selected_customer
                           , current_time=current_time, user_level=user_level, user_name=user_name, summary=summary)

def summary_ty(selected_product, selected_custno, start_date, end_date, user_ids):
    # ข้อมูล "มั่วๆ" สำหรับ summary_ty
    fake_data = []
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    brands = ['Brand X', 'Brand Y', 'Brand Z']
    uom = ['PCS', 'KG', 'LITER']

    # สร้างข้อมูล "มั่วๆ" 10 รายการ
    for i in range(10):
        matno = f'MAT{random.randint(1, 100)}'  # สุ่มหมายเลขสินค้า
        matname = random.choice(products)  # เลือกชื่อสินค้าจากรายการ
        brand = random.choice(brands)  # เลือกแบรนด์จากรายการ
        uprice = round(random.uniform(50, 200), 2)  # สุ่มราคา
        uom_convert = random.choice(uom)  # เลือกรูปแบบหน่วยจากรายการ

        # สร้างยอดขาย 12 เดือนแบบสุ่ม
        monthly_sales_qty = [random.randint(100, 1000) for _ in range(12)]  # จำนวนสินค้าตามเดือน
        monthly_sales_amt = [round(random.uniform(1000, 5000), 2) for _ in range(12)]  # ยอดขายตามเดือน

        # คำนวณยอดขายรวมและจำนวนรวม
        total_qty = sum(monthly_sales_qty)
        total_amt = sum(monthly_sales_amt)

        # สร้างข้อมูลในรูปแบบที่ต้องการ
        fake_data.append([matno, matname, brand, uprice, uom_convert] + monthly_sales_qty + monthly_sales_amt + [total_qty, total_amt])

    total_sum = sum(row[-1] for row in fake_data)  # รวมยอดขายทั้งหมด

    return fake_data, total_sum