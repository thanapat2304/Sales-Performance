from flask import render_template, session
from datetime import datetime
from backend.db_connection import connect_aep_DB
from backend.main_funtion import get_profile_picture_url
import random

def cusms_detail_py(row1, row10):
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    cusms_data = cusms_detail(row1, row10)
    ship_data = ship_detail(row1)

    if cusms_data:
        columns = [
            "shop_type", "custno", "custname", "custname_eng", "address", "email", "tel","fax", "custdesc", "contpers", "taxid",  "smdoce", "name", "smname2", "note", "line_ship"
        ]
        cusms_info = dict(zip(columns, cusms_data[0]))
    else:
        cusms_info = {}

    photo_url = get_profile_picture_url()

    return render_template('main/cusms_deail.html', current_time=current_time, user_name=user_name, user_level=user_level, cusms_info=cusms_info, ship_data=ship_data, photo_url=photo_url
                           ,user_moduals=user_moduals)

def cusms_detail(row1, row10):
    shop_types = ['Restaurant', 'Airline', 'Bakery', 'Company', 'Factory', 'Hotel', 'Individual', 'Other', 'WholeSale', 'Shopping Mall']
    
    customers = [
        {"CUSTNO": f"CUST{random.randint(1000, 9999)}", "CUSTNAME": f"Customer {random.randint(1, 100)}", "CUSTNAME_ENG": f"Customer {random.randint(1, 100)} ENG",
         "ADDRESS": f"Address {random.randint(1, 100)}", "TEL": f"0{random.randint(100000000, 999999999)}", "FAX": f"0{random.randint(100000000, 999999999)}", 
         "EMAIL": f"customer{random.randint(1, 100)}@example.com", "CUSTDESC": f"Description {random.randint(1, 100)}", 
         "CONTPERS": f"Contact {random.randint(1, 100)}", "TAXID": f"1234567890", "SMCODE": f"SM{random.randint(1, 10)}", 
         "SMNAME2": f"Salesman {random.randint(1, 10)}", "NOTETEXT": f"Note {random.randint(1, 10)}", "LINE_SHIP": f"Line {random.randint(1, 10)}"}
        for _ in range(5)
    ]
    
    for customer in customers:
        customer["SHOP TYPE"] = random.choice(shop_types)
    
    results = []
    for customer in customers:
        results.append((
            customer["SHOP TYPE"],
            customer["CUSTNO"],
            customer["CUSTNAME"],
            customer["CUSTNAME_ENG"],
            customer["ADDRESS"],
            customer["TEL"],
            customer["FAX"],
            customer["EMAIL"],
            customer["CUSTDESC"],
            customer["CONTPERS"],
            customer["TAXID"],
            customer["SMCODE"],
            customer["SMNAME2"],
            customer["NOTETEXT"],
            customer["LINE_SHIP"]
        ))

    return results
    
def ship_detail(row1):
    ship_addresses = [
        {"EXT": f"EXT{random.randint(1, 10)}", "ADD1": f"Shipping Address {random.randint(1, 100)}"}
        for _ in range(5)
    ]
    
    results = []
    for address in ship_addresses:
        results.append((
            address["EXT"],
            address["ADD1"]
        ))

    return results