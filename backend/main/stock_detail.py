from flask import render_template, session
from datetime import datetime, timedelta
from backend.db_connection import connect_aep_DB
from backend.main_funtion import get_profile_picture_url
import random

def stock_detail_py(row1, row8):
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    stock_data = stock_detail(row1, row8)
    ship_data = ship_detail(row1)
    mat = get_mat(row1)

    photo_url = get_profile_picture_url()

    return render_template('main/stock_datail.html', current_time=current_time, user_name=user_name, user_level=user_level, stock_data=stock_data, ship_data=ship_data, row1=row1, mat=mat
                           ,photo_url=photo_url, user_moduals=user_moduals)

def get_mat(row1):
    matno = f"{row1}"
    matdesc = f"Product Description {random.randint(1, 100)}"

    return f"{matno} | {matdesc}"

def stock_detail(row1, row8):
    stock_list = []
    for _ in range(random.randint(3, 7)):
        lot_no = f"LOT{random.randint(1000, 9999)}"
        expire_date = (datetime.today() + timedelta(days=random.randint(30, 365))).strftime('%d/%m/%Y')
        unit = f"{random.uniform(1, 100):,.2f}"
        whcode = row8
        whcode_desc = f"Warehouse {random.randint(1, 5)}"
        locode = f"LOC{random.randint(100, 999)}"

        stock_list.append((lot_no, expire_date, unit, whcode, whcode_desc, locode))

    return stock_list
    
def ship_detail(row1):
    # สุ่มจำนวน record ที่ต้องการจำลอง
    fake_rows = []
    for _ in range(random.randint(3, 6)):  # 3-6 รายการมั่วๆ
        unit = f"{random.uniform(10, 500):,.2f}"  # UNIT แบบตัวเลขทศนิยม 2 ตำแหน่ง
        ship_date = (datetime.today() + timedelta(days=random.randint(1, 90))).strftime('%d/%m/%Y')  # วันที่จัดส่งในอนาคต
        po_status = random.choice(['Pending', 'In Transit', 'Confirmed', 'Waiting'])  # สถานะที่ไม่ใช่ 'Complete' หรือ ''

        fake_rows.append((unit, ship_date, po_status))

    return fake_rows