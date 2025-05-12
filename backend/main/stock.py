from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import random

def stock_master():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    results = None
    show_all = None
    selected_product = None
    selected_wh = None
    selected_mat = None
    selected_weaho = None
    
    if request.method == 'POST':
        selected_product = request.form['product']
        selected_wh = request.form['wh']
        selected_mat = request.form.get('product')
        selected_weaho = request.form.get('wh')
        show_all = request.form.get('all')

        results = master_mat(selected_product, selected_wh, show_all)

    product1, product2 = get_product()
    wh1, wh2 = get_wh()
    photo_url = get_profile_picture_url()

    return render_template('main/stock.html', current_time=current_time, user_name=user_name, user_level=user_level, product1=product1, product2=product2, wh1=wh1, wh2=wh2, results=results,
                           selected_mat=selected_mat, selected_weaho=selected_weaho, show_all=show_all, photo_url=photo_url, user_moduals=user_moduals)

def master_mat(selected_product, selected_wh, show_all):
    brands = ['BrandA', 'BrandB', 'BrandC']
    uoms = ['PCS', 'BOX', 'SET']
    locodes = ['L001', 'L002', 'L003', 'L004']
    whcodes = ['WH101', 'WH102', 'WH103']
    
    data = []
    for _ in range(15):
        matno = f"MAT{random.randint(1000, 9999)}"
        matdesc = f"Product Description {random.randint(1, 100)}"
        
        row = (
            random.choice(brands),
            matno,
            matdesc,
            f"{random.uniform(0, 100):,.2f}",
            random.choice(uoms),
            f"{random.uniform(0, 50):,.2f}",
            f"{random.uniform(0, 30):,.2f}",
            f"{random.uniform(10, 500):,.2f}",
            random.choice(whcodes),
            random.choice(locodes)
        )
        data.append(row)

    return data

def get_product():
    products = [
        {"MATNO": f"MAT{random.randint(1000, 9999)}", "MATDESC": f"Product Description {random.randint(1, 100)}"}
        for _ in range(10)
    ]
    
    product1 = [product["MATNO"] for product in products]
    product2 = [f"{product['MATNO']} | {product['MATDESC']}" for product in products]
    
    product1.insert(0, "ALL")
    product2.insert(0, "ALL | สินค้าทั้งหมด")

    return product1, product2

def get_wh():
    warehouses = [
        {"WHCODE": f"WH{random.randint(100, 999)}", "DESCR": f"Warehouse {random.randint(1, 100)}"}
        for _ in range(10)
    ]
    
    wh1 = [warehouse["WHCODE"] for warehouse in warehouses]
    wh2 = [f"{warehouse['WHCODE']} | {warehouse['DESCR']}" for warehouse in warehouses]

    wh1.insert(0, "ALL")
    wh2.insert(0, "ALL | คลังทั้งหมด")

    return wh1, wh2