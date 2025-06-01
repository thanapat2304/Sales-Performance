from flask import render_template, session, send_file, request, redirect, url_for
import xlwings as xw
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import pandas as pd
import os

def oneonone_branch():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    photo_url = get_profile_picture_url()
    start_date = None
    end_date = None

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        return redirect(url_for('export.download_branch_oneonone', start_date=start_date, end_date=end_date))

    return render_template('export_report/oneononebranch.html', user_name=user_name, user_level=user_level, current_time=current_time, photo_url=photo_url, user_moduals=user_moduals)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'from')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def download_oneonone_branch(start_date, end_date):
    data = get_oneonone_branch_data(start_date, end_date)
    
    if data is None:
        return "Error: ไม่สามารถดึงข้อมูลได้", 500

    df = pd.DataFrame(data)
    
    excel_path = os.path.join(OUTPUT_FOLDER, "OneOnOne_Branch.xlsx")
    excel_file_path = os.path.join(DOWNLOAD_FOLDER, 'From_OneOnOne_Branch.xlsx')

    if not os.path.exists(excel_file_path):
        return "Error: Excel file not found", 400
    
    app_xw = xw.App(visible=False)
    try:
        workbook = app_xw.books.open(excel_file_path)
        sheet = workbook.sheets['Data']

        sheet.range("A67605").value = df.values

        all_sheet = workbook.sheets['SUM ALL']
        all_sheet.api.PivotTables("ALL").RefreshTable()

        customer_sheet = workbook.sheets['Sum of Customer']
        customer_sheet.api.PivotTables("Customer").RefreshTable()

        product_sheet = workbook.sheets['Sum of Product']
        product_sheet.api.PivotTables("Product").RefreshTable()

        Pro_Cust_sheet = workbook.sheets['Sum Of Product+Cus']
        Pro_Cust_sheet.api.PivotTables("Pro_Cust").RefreshTable()

        History_sheet = workbook.sheets['Sale History']
        History_sheet.api.PivotTables("History").RefreshTable()

        workbook.save(excel_path)

    finally:
        if workbook:
            workbook.close()
        if app_xw:
            app_xw.quit()

    return send_file(excel_path, as_attachment=True)

def OneOnOne_Phuket(start_date, end_date):
    conn = connect_aep_DB()
    if conn is None:
        return None

    query = """
        SELECT * FROM customers WHERE customer_id = 12345;
    """

    try:
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    except Exception as e:
        return None
    
def OneOnOne_Phetchaburi(start_date, end_date):
    conn = connect_aep_DB()
    if conn is None:
        return None

    query = """
        SELECT * FROM customers WHERE customer_id = 12345;
    """

    try:
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    except Exception as e:
        return None
    
def OneOnOne_Sikhio(start_date, end_date):
    conn = connect_aep_DB()
    if conn is None:
        return None

    query = """
        SELECT * FROM customers WHERE customer_id = 12345;
    """

    try:
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    except Exception as e:
        return None
    
def OneOnOne_Sriracha(start_date, end_date):
    conn = connect_aep_DB()
    if conn is None:
        return None

    query = """
        SELECT * FROM customers WHERE customer_id = 12345;
    """

    try:
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    except Exception as e:
        return None
    
def OneOnOne_Udon(start_date, end_date):
    conn = connect_aep_DB()
    if conn is None:
        return None

    query = """
        SELECT * FROM customers WHERE customer_id = 12345;
    """

    try:
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    except Exception as e:
        return None
    
def get_oneonone_branch_data(start_date, end_date):
    Phuket = OneOnOne_Phuket(start_date, end_date)
    Phetchaburi = OneOnOne_Phetchaburi(start_date, end_date)
    Sikhio = OneOnOne_Sikhio(start_date, end_date)
    Srirach = OneOnOne_Sriracha(start_date, end_date)
    Udon = OneOnOne_Udon(start_date, end_date)

    data = pd.concat([Phuket, Phetchaburi, Sikhio, Srirach, Udon], ignore_index=True)

    df = pd.DataFrame(data)

    return df