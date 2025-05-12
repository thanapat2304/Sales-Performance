from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.pivot.summary_cus import get_salesman, get_customers, get_selected_salesman_info, all_customers
from backend.main.stock import get_product
from backend.main_funtion import get_profile_picture_url
import random

def summary_item():
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
    selected_salesman = None
    selected_salesman_info = None
    selected_sm = None
    selected_product = None
    selected_custno = None
    selected_mat = None
    selected_customer = None

    if request.method == 'POST':
        selected_salesman = request.form['salesman']
        selected_product = request.form['product']
        selected_custno = request.form['customer']
        bill_date = request.form['date']
        selected_sm = request.form.get('salesman')
        selected_mat = request.form.get('product')
        selected_customer = request.form.get('customer')

    if bill_date:
        start_date_str, end_date_str = bill_date.split(' - ')
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y').strftime('%Y/%m/%d')
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y').strftime('%Y/%m/%d')
    else:
        start_date = None
        end_date = None

    selected_salesman_info = get_selected_salesman_info(selected_salesman)
    summary, total_sum = summary_ty(selected_salesman, selected_product, selected_custno, start_date, end_date, user_ids)
    salesman1, salesman2 = get_salesman(user_ids, user_level)
    customers1, customers2 = get_customers(user_ids)
    product1, product2 = get_product()
    photo_url = get_profile_picture_url()

    return render_template('pivot/summary_item.html', customers1=customers1, customers2=customers2, salesman1=salesman1, salesman2=salesman2, product2=product2, user_moduals=user_moduals
                           ,selected_salesman_info=selected_salesman_info, total_sum=total_sum, product1=product1, selected_mat=selected_mat, selected_customer=selected_customer
                           , current_time=current_time, user_level=user_level, user_name=user_name, selected_sm=selected_sm, summary=summary, photo_url=photo_url)

def summary_ty(selected_salesman, selected_product, selected_custno, start_date, end_date, user_ids):
    fake_data = []
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    uom = ['PCS', 'KG', 'LITER']

    for i in range(10):
        matno = f'MAT{random.randint(1, 100)}'
        matname = random.choice(products)
        uom_convert = random.choice(uom)

        monthly_sales_qty = [random.randint(100, 1000) for _ in range(12)]
        monthly_sales_amt = [round(random.uniform(1000, 5000), 2) for _ in range(12)]

        total_qty = sum(monthly_sales_qty)
        total_amt = sum(monthly_sales_amt)

        fake_data.append([matno, matname, uom_convert] + monthly_sales_qty + monthly_sales_amt + [total_qty, total_amt])

    total_sum = sum(row[-1] for row in fake_data)

    return fake_data, total_sum