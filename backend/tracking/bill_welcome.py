from flask import render_template, session
from backend.db_connection import connect_aep_DB
from backend.main_funtion import get_profile_picture_url
import random
from datetime import datetime, timedelta

def bill_detail_py(docno):
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    bill_data = bill_detail(docno)

    if bill_data:
        columns = [
            "doc_date", "due_date", "doc_no", "cust_code", "cust_name", "cust_eng","po_no", "ship_address", "sales_code", "sales_name",  "ship_to", "remark"
        ]
        bill_info = dict(zip(columns, bill_data[0]))
        subtotal = sum(float(row[19].replace(',', '')) for row in bill_data)
        subtotal_formatted = f"{subtotal:,.2f}"

        discount = sum(float(row[18].replace(',', '')) for row in bill_data)
        discount_formatted = f"{discount:,.2f}"

        vat = sum(float(row[20].replace(',', '')) for row in bill_data)
        vat_formatted = f"{vat:,.2f}"

        total = subtotal - discount
        total_formatted = f"{total:,.2f}"

        Grand_total = subtotal + vat
        Grand_total_formatted = f"{Grand_total:,.2f}"
    else:
        bill_info = {}
        subtotal_formatted = "0"
        discount_formatted = "0"
        vat_formatted = "0"
        total_formatted = "0"
        Grand_total_formatted = "0"

    photo_url = None

    return render_template('dashboard_user/bill_welcome.html', current_time=current_time, bill_data=bill_data, docno=docno, user_name=user_name, user_level=user_level, bill_info=bill_info,
                           subtotal_formatted=subtotal_formatted, discount_formatted=discount_formatted, vat_formatted=vat_formatted, total_formatted=total_formatted, photo_url=photo_url
                           , Grand_total_formatted=Grand_total_formatted)

def bill_detail(docno):
    num_items = random.randint(3, 7)

    today = datetime.today()

    result = []

    for i in range(1, num_items + 1):
        doc_date = today.strftime("%d/%m/%Y")
        due_date = (today + timedelta(days=random.randint(15, 60))).strftime("%d/%m/%Y")
        doc_number = f"TX{random.randint(100000000, 999999999)}"
        cust_code = f"CUST{random.randint(1000, 9999)}"
        cust_name = f"บริษัทตัวอย่าง {random.randint(1, 99)}"
        cust_name_eng = random.choice(["Google", "Nike", "Tesla", "Microsoft"])
        po_no = f"PO{random.randint(100000000, 999999999)}"
        ship_address = random.choice(["ถนนสุขุมวิท 24 กรุงเทพมหานคร 10110", "ถนนพระราม กรุงเทพมหานคร 10310"])
        sales_code = f"SM{random.randint(10, 99)}"
        sales_name = f"Salesperson {random.randint(1, 50)}"
        ship_to = random.choice(["123/45 ถนนสุขุมวิท 24 แขวงคลองตัน เขตคลองเตย กรุงเทพมหานคร 10110", "678/9 ถนนพระราม 9 แขวงบางกะปิ เขตห้วยขวาง กรุงเทพมหานคร 10310"])
        remark = f"Remark {random.randint(1, 5)}"
        ext_no = str(i)
        prod_code = f"PROD{random.randint(10000, 99999)}"
        prod_name = f"Product {random.randint(1, 50)}"
        qty = random.randint(1, 50)
        uom = random.choice(["PCS", "BOX", "PACK"])
        unit_price = random.randint(100, 2000)
        discount = random.randint(0, 100)
        amount = qty * unit_price
        vat = int(amount * 0.07)
        net_amount_novat = amount - discount
        net_amount_calculated = (amount - discount) + vat

        row = (
            doc_date,
            due_date,
            doc_number,
            cust_code,
            cust_name,
            cust_name_eng,
            po_no,
            ship_address,
            sales_code,
            sales_name,
            ship_to,
            remark,
            ext_no,
            prod_code,
            prod_name,
            str(qty),
            uom,
            f"{unit_price:,}",
            f"{discount:,}",
            f"{amount:,}",
            f"{vat:,}",
            f"{net_amount_novat:,}",
            f"{net_amount_calculated:,}",
        )
        result.append(row)

    return result