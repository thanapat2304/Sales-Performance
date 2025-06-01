import os
from flask import url_for, session
from backend.db_connection import connect_aep_portal, connect_aep_DB
from datetime import datetime
import random

def get_profile_picture_url():
    return url_for('static', filename='img/test1.jpg')

def get_all_sales_target():
    connection = connect_aep_portal()
    cursor = connection.cursor()
    
    cursor.execute("SELECT RPS_Target_id FROM rps_tb_target")
    target_ids = cursor.fetchall()
    
    target_ids_list = [str(id[0]) for id in target_ids]
    target_ids_str = ','.join(target_ids_list) if target_ids_list else None
    
    cursor.close()
    connection.close()
    
    return target_ids_str

def get_brand():
    return [
        "Agriform",
        "Bridor",
        "CACAO BARRY",
        "COLAVITA",
        "DARBO",
        "ELLE&VIRE",
        "GMP",
        "Milkana",
        "Others",
        "PONTHIER",
        "PreGel",
        "VAN HOUTEN"
    ]

def get_top():
    return [
        "10",
        "20",
        "50",
        "100"
    ]

def get_years():
    current_year = datetime.now().year
    start_year = current_year - 2
    years = [{'id': str(year), 'AS_Name_year': str(year)} for year in range(current_year, start_year - 1, -1)]
    return years

def get_year_compare():
    current_year = datetime.now().year
    year_ranges = [f"{year}-{year+1}" for year in range(current_year - 3, current_year)]  
    return year_ranges

def get_salesman(user_ids, user_level):
    salesman1 = [f"SM{str(i+1).zfill(3)}" for i in range(10)]
    salesman2 = [f"{sm} | Salesman {i+1}" for i, sm in enumerate(salesman1)]

    salesman1.insert(0, "ALL")
    salesman2.insert(0, "ALL | ผู้ขายทั้งหมด")

    return salesman1, salesman2

def all_customers(user_ids):
    conn = connect_aep_DB()
    cursor = conn.cursor()

    placeholders = ','.join(['%s'] * len(user_ids))
    query = f"""SELECT * FROM customers WHERE customer_id = 12345;"""

    cursor.execute(query, user_ids)
    allcustomers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return allcustomers

def get_product():
    conn = connect_aep_DB()
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM customers WHERE customer_id = 12345;""")
    product1 = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("""SELECT * FROM customers WHERE customer_id = 12345;""")
    product2 = [row[0] for row in cursor.fetchall()]
    
    product1.insert(0, "ALL")
    product2.insert(0, "ALL | สินค้าทั้งหมด")

    conn.close()

    return product1, product2

def get_salesman_all():
    # ชื่อสุ่ม
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Hannah']
    
    salesman1 = []
    salesman2 = []

    for i in range(20):  # สร้างข้อมูลสุ่ม 20 รายการ
        smcode = f"SM{1000 + i}"
        name = random.choice(names)
        
        salesman1.append(smcode)
        salesman2.append(f"{smcode} | {name}")

    return salesman1, salesman2

def get_years_up_down_one():
    current_year = datetime.now().year
    start_year = current_year - 1
    end_year = current_year + 1
    years = [{'id': str(year), 'AS_Name_year': str(year)} for year in range(start_year, end_year + 1)]
    return years