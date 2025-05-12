from flask import render_template, session, send_file, request, redirect, url_for
import xlwings as xw
from backend.db_connection import connect_aep_DB, connect_aep_portal
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import pandas as pd
import os

def main_Target_Actual():
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

        return redirect(url_for('export.download_Actual_Target', start_date=start_date, end_date=end_date))

    return render_template('export_report/Target_Actual.html', user_name=user_name, user_level=user_level, current_time=current_time, photo_url=photo_url, user_moduals=user_moduals)

def get_start_date(end_date):
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = end_dt.replace(day=1)
    return start_date.strftime("%Y-%m-%d")

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'from')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def download_Target_Actual(start_date, end_date):
    data_raw_sales = data_sale(start_date, end_date)
    data_raw_target = process_sales_data(start_date, end_date)
    data_raw_sample = data_sample(end_date)
    data_raw_status = data_status()
    
    df_target = pd.DataFrame(data_raw_target)
    df_sample = pd.DataFrame(data_raw_sample)
    df_status = pd.DataFrame(data_raw_status)
    df = pd.DataFrame(data_raw_sales)
    
    excel_path = os.path.join(OUTPUT_FOLDER, "Sales_report_target&actual.xlsx")
    excel_file_path = os.path.join(DOWNLOAD_FOLDER, 'From_Target&Actual.xlsx')

    if not os.path.exists(excel_file_path):
        return "Error: Excel file not found", 400
    
    app_xw = xw.App(visible=False)
    try:
        workbook = app_xw.books.open(excel_file_path)

        DataSalesTarget = workbook.sheets['DataSalesTarget']
        DataSalesTarget.range("A2").value = df_target.values

        Data_Sales = workbook.sheets['Data Sales']
        Data_Sales.range("A216133").value = df.values

        Data_Sample = workbook.sheets['Data Sample']
        Data_Sample.range("A2").value = df_sample.values

        Status = workbook.sheets['Status']
        Status.range("A2").value = df_status.values

        Compare_custype = workbook.sheets['Compare custype']
        Compare_custype.api.PivotTables("custype_old").RefreshTable()
        Compare_custype.api.PivotTables("custype_new").RefreshTable()

        Sales_report = workbook.sheets['Sales report (Target&Actual)']
        Sales_report.api.PivotTables("Sales_report_1").RefreshTable()
        Sales_report.api.PivotTables("Sales_report_2").RefreshTable()

        Chart_tb = workbook.sheets['Chart']
        Chart_tb.api.PivotTables("chart_tb").RefreshTable()

        Top10 = workbook.sheets['Top10 Customer B-Sales']
        Top10.api.PivotTables("Top10_tb").RefreshTable()

        Report_sample = workbook.sheets['Report sample']
        Report_sample.api.PivotTables("sample_1").RefreshTable()
        Report_sample.api.PivotTables("sample_2").RefreshTable()

        workbook.save(excel_path)

    finally:
        if workbook:
            workbook.close()
        if app_xw:
            app_xw.quit()

    return send_file(excel_path, as_attachment=True)

def data_sale(start_date, end_date):
    conn = connect_aep_DB()
    if conn is None:
        return None

    query = """
        SELECT
            DAY(INQ_SALEREPORT_RAWDATA_GTAP_NEW.DOCDATE) AS Day,
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.MNT, 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.YR, 	
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO, 
            ARCODE.CUSTNAME, 
            CASE INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTYPE
                WHEN 'Airline (สายการบิน)' THEN 'Airline'
                WHEN 'Bakery Shop (ร้านเบเกอรี่)' THEN 'Bakery Shop'
                WHEN 'Company (บริษัท)' THEN 'Company'
                WHEN 'Factory (โรงงาน)' THEN 'Factory'
                WHEN 'Hotel (โรงแรม)' THEN 'Hotel'
                WHEN 'Individual (บุคคล)' THEN 'Individual'
                WHEN 'Other' THEN 'Other'
                WHEN 'Restaurant - American' THEN 'Restaurant'
                WHEN 'Restaurant - Chinese (ร้านอาหารจีน)' THEN 'Restaurant'
                WHEN 'Restaurant - Europe' THEN 'Restaurant'
                WHEN 'Restaurant - Frence (ร้านอาหารฝรั่งเศส)' THEN 'Restaurant'
                WHEN 'Restaurant - German' THEN 'Restaurant'
                WHEN 'Restaurant - Italian (ร้านอาหารอิตาเลี่ยน)' THEN 'Restaurant'
                WHEN 'Restaurant - Japanese (ร้านอาหารญี่ปุ่น)' THEN 'Restaurant'
                WHEN 'Restaurant - Korean' THEN 'Restaurant'
                WHEN 'Restaurant - Mexican' THEN 'Restaurant'
                WHEN 'Restaurant - Spain' THEN 'Restaurant'
                WHEN 'Restaurant - Thai (ร้านอาหารไทย)' THEN 'Restaurant'
                WHEN 'Restaurant - มุสลิม/อิสลาม' THEN 'Restaurant'
                WHEN 'Restaurant - ร้านอาหารทั่วไป' THEN 'Restaurant'
                WHEN 'Retail Event' THEN 'Retail Event'
                WHEN 'School  (โรงเรียน)' THEN 'School'
                WHEN 'Whole Sale Shop (ร้านขายส่ง)' THEN 'Whole Sale Shop'
                WHEN 'ห้างสรรพสินค้า' THEN 'Supermarket'
            END AS End_Customer_Type,
            ARCODE.SMCODE AS SMCODE_MASTER, 
            ARSALMAN.NAME AS SMNAME_MASTER, 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.NETAMOUNT AS AMOUNT
        FROM
            dbo.INQ_SALEREPORT_RAWDATA_GTAP_NEW
        LEFT JOIN
            dbo.ARCODE
        ON 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO = ARCODE.CUSTNO
        LEFT JOIN
            dbo.ARSALMAN
        ON 
            ARCODE.COCODE = ARSALMAN.COCODE AND
            ARCODE.SMCODE = ARSALMAN.SMCODE
        WHERE
            ARCODE.COCODE = 'AEPC' AND
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.DOCDATE BETWEEN %s AND %s AND
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.MATNO <> 'CANCEL' 
        ORDER BY DOCDATE DESC	
    """

    try:
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    except Exception as e:
        return None
    
def data_target():
    conn = connect_aep_portal()
    if conn is None:
        return None

    query = """
    SELECT 
        RPS_Target_YR,
        RPS_Target_id,
        RPS_Target_Name,
        RPS_Jan,
        RPS_Feb,
        RPS_Mar,
        RPS_Apr,
        RPS_May,
        RPS_Jun,
        RPS_Jul,
        RPS_Aug,
        RPS_Sep,
        RPS_Oct,
        RPS_Nov,
        RPS_Dec
    FROM rps_tb_target
    WHERE RPS_Target_YR = YEAR(CURRENT_DATE)
    """

    try:
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    except Exception as e:
        return None
    
def data_status():
    conn = connect_aep_portal()
    if conn is None:
        return None

    query = """
    SELECT 
        SMCODE_status,
        SMNAME_status,
        REMARK_status, 
        NICKNAME_status
    FROM tb_status_sales
    """

    try:
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    except Exception as e:
        return None
    
def data_sample(end_date):
    start_date = get_start_date(end_date)
    conn = connect_aep_DB()
    if conn is None:
        return None

    query = """
    SELECT
        DAY(INQ_SO_PAYGIFT_FULL.DOCDATE) AS DAY,
        INQ_SO_PAYGIFT_FULL.YR, 
        INQ_SO_PAYGIFT_FULL.MNT,
        INQ_SO_PAYGIFT_FULL.CUSTNO, 
        INQ_SO_PAYGIFT_FULL.CUSTNAME, 
        INQ_SO_PAYGIFT_FULL.SMCODE, 
        INQ_SO_PAYGIFT_FULL.SMNAME,
        INQ_SO_PAYGIFT_FULL.MATNO, 
        INQ_SO_PAYGIFT_FULL.MATDESC, 
        INQ_SO_PAYGIFT_FULL.UNIT, 
        INQ_SO_PAYGIFT_FULL.UOM_DESC
    FROM
        dbo.INQ_SO_PAYGIFT_FULL
    WHERE 
        INQ_SO_PAYGIFT_FULL.COCODE = 'AEPC' AND
    INQ_SO_PAYGIFT_FULL.DOCDATE BETWEEN %s AND %s
    """

    try:
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    except Exception as e:
        return None
    
def process_sales_data(start_date, end_date):
    sale = data_sale(start_date, end_date)
    target = data_target()
    status = data_status()
    data_old = pd.read_excel( r'C:\Users\thanapurt.so\Desktop\Report_AEP\Target&Actual\data2024\2024.xlsx')
    
    month_mapping = {
        "RPS_Jan": 1, "RPS_Feb": 2, "RPS_Mar": 3, "RPS_Apr": 4,
        "RPS_May": 5, "RPS_Jun": 6, "RPS_Jul": 7, "RPS_Aug": 8,
        "RPS_Sep": 9, "RPS_Oct": 10, "RPS_Nov": 11, "RPS_Dec": 12
    }
    
    df_target = target.melt(
        id_vars=["RPS_Target_YR", "RPS_Target_id", "RPS_Target_Name"],
        value_vars=[
            "RPS_Jan", "RPS_Feb", "RPS_Mar", "RPS_Apr", "RPS_May", "RPS_Jun",
            "RPS_Jul", "RPS_Aug", "RPS_Sep", "RPS_Oct", "RPS_Nov", "RPS_Dec"
        ],
        var_name="RPS_Target_MNT",
        value_name="target"
    )
    
    df_target["RPS_Target_MNT"] = df_target["RPS_Target_MNT"].map(month_mapping)
    
    data_old['SMCODE_MASTER'] = data_old['SMCODE_MASTER'].astype(str)
    
    raw_data = pd.concat([data_old, sale])
    
    pivot_table = raw_data.pivot_table(
        index=['MNT', 'SMCODE_MASTER', 'SMNAME_MASTER'],
        columns='YR',
        values='AMOUNT',
        aggfunc='sum',
        fill_value=0
    )
    
    pivot_df = pivot_table.reset_index()
    pivot_df = pivot_df.rename(columns={pivot_df.columns[-2]: "Old", pivot_df.columns[-1]: "New"})
    
    merged_df = pivot_df.merge(
        status[['SMCODE_status', 'REMARK_status', 'NICKNAME_status']],
        left_on='SMCODE_MASTER', 
        right_on='SMCODE_status', 
        how='left'
    )
    
    merged_df = merged_df[['MNT', 'SMCODE_MASTER', 'SMNAME_MASTER', 'Old', 'New', 'REMARK_status', 'NICKNAME_status']]
    merged_df = merged_df[merged_df['REMARK_status'].ne('Non Active')]
    
    df_target['RPS_Target_id'] = df_target['RPS_Target_id'].astype(str)
    data_use = merged_df.merge(
        df_target[['RPS_Target_id', 'RPS_Target_MNT', 'target']],
        left_on=['SMCODE_MASTER', 'MNT'], 
        right_on=['RPS_Target_id', 'RPS_Target_MNT'], 
        how='left'
    )
    
    data_use = data_use.drop(columns=['RPS_Target_id', 'RPS_Target_MNT'])
    data_use = data_use[data_use['New'] != 0]
    data = data_use[['SMCODE_MASTER','SMNAME_MASTER','NICKNAME_status','MNT','target','Old','New','REMARK_status']]
    
    return data