from flask import render_template, session, send_file, request, redirect, url_for
import xlwings as xw
from backend.db_connection import connect_aep_DB
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import pandas as pd
import os

def oneonone_sales():
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

        return redirect(url_for('export.download_sales_oneonone', start_date=start_date, end_date=end_date))

    return render_template('export_report/oneononesales.html', user_name=user_name, user_level=user_level, current_time=current_time, photo_url=photo_url, user_moduals=user_moduals)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'from')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def download_oneonone_sales(start_date, end_date):
    data = OneOnOne_Nok(start_date, end_date)
    
    if data is None:
        return "Error: ไม่สามารถดึงข้อมูลได้", 500

    df = pd.DataFrame(data)
    
    excel_path = os.path.join(OUTPUT_FOLDER, "All_Sales_report_compare.xlsx")
    excel_file_path = os.path.join(DOWNLOAD_FOLDER, 'From_OneOnOne_Sales.xlsx')

    if not os.path.exists(excel_file_path):
        return "Error: Excel file not found", 400
    
    app_xw = xw.App(visible=False)
    try:
        workbook = app_xw.books.open(excel_file_path)
        sheet = workbook.sheets['Data']

        sheet.range("A589357").value = df.values

        sum_sheet = workbook.sheets['SUM']
        sum_sheet.api.PivotTables("SUM_TABLE").RefreshTable()

        customer_sheet = workbook.sheets['Customer By Sales']
        customer_sheet.api.PivotTables("CUST_TABLE").RefreshTable()

        workbook.save(excel_path)

    finally:
        if workbook:
            workbook.close()
        if app_xw:
            app_xw.quit()

    return send_file(excel_path, as_attachment=True)

def OneOnOne_Nok(start_date, end_date):
    conn = connect_aep_DB()
    if conn is None:
        return None

    query = """
        SELECT
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.DT,
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.DOCDATE, 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.MNT,
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.YR,
            CONCAT(INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO,' | ',ARCODE.CUSTNAME) AS CUSTOMER,
            CONCAT(INQ_SALEREPORT_RAWDATA_GTAP_NEW.SMCODE,' | ',INQ_SALEREPORT_RAWDATA_GTAP_NEW.SMNAME) AS SALESMAN, 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.NETAMOUNT AS AMOUNT,
            CASE 
                INQ_SALEREPORT_RAWDATA_GTAP_NEW.SMCODE
                WHEN '20000' THEN 'Account'
                WHEN '10377' THEN 'Chin'
                WHEN '10237' THEN 'Candy'
                WHEN '10017' THEN 'Nok'
                WHEN '10016' THEN 'Noom'
                WHEN '10246' THEN 'Joke'
                WHEN '10181' THEN 'Zen'
                WHEN '10015' THEN 'Mind'
                WHEN '10195' THEN 'Pik'
                WHEN '10067' THEN 'Pear'
                WHEN '10310' THEN 'Grip'
                WHEN '10313' THEN 'Nui'
                WHEN '10304' THEN 'June'
                WHEN '19999' THEN 'Office'
                WHEN '10339' THEN 'Pom'
                WHEN '10305' THEN 'Miew'
                WHEN '10025' THEN 'Koy'
                WHEN '10120' THEN 'Laor'
                WHEN '10359' THEN 'Tak'
                WHEN '10362' THEN 'Oat(Thanabordee)'
                WHEN '10382' THEN 'Fai'
                WHEN '10383' THEN 'Put'
                WHEN '10153' THEN 'Nut (BD)'
                WHEN '19998' THEN 'Suvit (BD)'
                WHEN '10001' THEN 'Suvit (Suvit)'
                WHEN '19996' THEN 'Suvit (Mind)'
                WHEN '19995' THEN 'Sale-C'
                WHEN '10132' THEN 'Support Sale'
                WHEN '10363' THEN 'Took'
                WHEN '10370' THEN 'Yim'
                WHEN '10229' THEN 'Ying'
                WHEN '10352' THEN 'Zin'
                WHEN '10354' THEN 'Klao'
                WHEN '10403' THEN 'Bam'
                WHEN '10413' THEN 'Oat(Vatchalakorn)'
                WHEN '10416' THEN 'Pop'
                WHEN '10423' THEN 'Pat'
                WHEN '10433' THEN 'Ice'
                WHEN '10446' THEN 'Aei'
                WHEN '10450' THEN 'Pan'
                WHEN '10130' THEN 'Dao'
                WHEN '10143' THEN 'Bell(Nida)'
                WHEN '10194' THEN 'Maury'
                WHEN '10296' THEN 'Peat'
                WHEN '10415' THEN 'Chomphu'
                WHEN '10432' THEN 'Benz'
                WHEN '10444' THEN 'Luktan'
                WHEN '19992' THEN 'Bell(Kanlaya)'
                WHEN '20002' THEN 'Europe'
                WHEN '20003' THEN 'Phuripat'
                WHEN '10367' THEN 'Kim'
                WHEN '10240' THEN 'Biw'
                WHEN '10325' THEN 'Pu'
                WHEN '10210' THEN 'Golf(Chatchai)'
                WHEN '10024' THEN 'Santi'
                WHEN '10024' THEN 'Santi'
                WHEN '10400' THEN 'Bell(Warisara)'
                WHEN '10084' THEN 'Pang'
                WHEN '10220' THEN 'Rat'
                WHEN '10460' THEN 'Mook'
            END AS TAG_SALEs

        FROM
            dbo.INQ_SALEREPORT_RAWDATA_GTAP_NEW
        LEFT JOIN
            dbo.ARCODE
        ON 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO = ARCODE.CUSTNO
        WHERE
            ARCODE.COCODE = 'AEPC' AND
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.DOCDATE BETWEEN %s AND %s
    """

    try:
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df
    except Exception as e:
        return None