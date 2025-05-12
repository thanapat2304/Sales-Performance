from flask import render_template, session
from datetime import datetime
from backend.db_connection import connect_aep_DB
from backend.main_funtion import get_profile_picture_url

def power_product_detail(matno_value, smcode_value):
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    query_customer_name = """
    SELECT TOP 1 MATDESC
    FROM IMMATMAS
    WHERE MATNO = %s
    """
    
    query1 = """
    SELECT 
        T.CUSTNO, 
        T.CUSTNAME, 
        MAX(T.DOCDATE) AS LastPurchaseDate,
        MAX(CASE WHEN T.DOCDATE = T.MAX_DOCDATE THEN T.NETAMOUNT END) AS LastPurchaseAmount
    FROM (
        SELECT 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO, 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNAME, 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.DOCDATE, 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.NETAMOUNT,
            MAX(INQ_SALEREPORT_RAWDATA_GTAP_NEW.DOCDATE) OVER (PARTITION BY INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO, INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNAME) AS MAX_DOCDATE
        FROM dbo.INQ_SALEREPORT_RAWDATA_GTAP_NEW 
        LEFT JOIN dbo.ARCODE ON INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO = ARCODE.CUSTNO
        WHERE INQ_SALEREPORT_RAWDATA_GTAP_NEW.MATNO = %s
		    AND ARCODE.SMCODE IN %s
        AND INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO NOT IN (
            SELECT DISTINCT INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO
            FROM INQ_SALEREPORT_RAWDATA_GTAP_NEW
            WHERE INQ_SALEREPORT_RAWDATA_GTAP_NEW.MATNO = %s
            AND ARCODE.SMCODE IN %s
            AND INQ_SALEREPORT_RAWDATA_GTAP_NEW.YR < YEAR(GETDATE()) - 1
        )
        AND INQ_SALEREPORT_RAWDATA_GTAP_NEW.YR IN (YEAR(GETDATE()) - 1, YEAR(GETDATE()))
        AND INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO <> 'CANCEL'
    ) T
    GROUP BY T.CUSTNO, T.CUSTNAME
    ORDER BY LastPurchaseDate DESC;
    """
    
    query2 = """
    SELECT 
        T.CUSTNO, 
        T.CUSTNAME, 
        MAX(T.DOCDATE) AS LastPurchaseDate,
        MAX(CASE WHEN T.DOCDATE = T.MAX_DOCDATE THEN T.NETAMOUNT END) AS LastPurchaseAmount
    FROM (
        SELECT 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO, 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNAME, 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.DOCDATE, 
            INQ_SALEREPORT_RAWDATA_GTAP_NEW.NETAMOUNT,
            MAX(INQ_SALEREPORT_RAWDATA_GTAP_NEW.DOCDATE) OVER (PARTITION BY INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO, INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNAME) AS MAX_DOCDATE
        FROM dbo.INQ_SALEREPORT_RAWDATA_GTAP_NEW 
        LEFT JOIN dbo.ARCODE ON INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO = ARCODE.CUSTNO
        WHERE INQ_SALEREPORT_RAWDATA_GTAP_NEW.MATNO = %s
        AND ARCODE.SMCODE IN %s
        AND INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO NOT IN (
            SELECT DISTINCT INQ_SALEREPORT_RAWDATA_GTAP_NEW.CUSTNO
            FROM INQ_SALEREPORT_RAWDATA_GTAP_NEW
            WHERE INQ_SALEREPORT_RAWDATA_GTAP_NEW.MATNO = %s
            AND ARCODE.SMCODE IN %s
            AND INQ_SALEREPORT_RAWDATA_GTAP_NEW.DOCDATE >= DATEADD(MONTH, -2, GETDATE())
        )
    ) T
    GROUP BY T.CUSTNO, T.CUSTNAME
    ORDER BY LastPurchaseDate DESC;
    """
    if smcode_value:
        smcode_value = (smcode_value,)
    else:
        smcode_value = ()
    
    conn = connect_aep_DB()
    cursor = conn.cursor()
    
    cursor.execute(query_customer_name, (matno_value,))
    custname = cursor.fetchone()
    custname = custname[0] if custname else "Unknown Customer"
    
    cursor.execute(query1, (matno_value, smcode_value, matno_value, smcode_value))
    results1 = cursor.fetchall()
    
    cursor.execute(query2, (matno_value, smcode_value, matno_value, smcode_value))
    results2 = cursor.fetchall()
    
    conn.close()

    photo_url = get_profile_picture_url()
    
    return render_template(
        'dashboard_user/detail_topmat.html', 
        purchase_data1=results1, 
        purchase_data2=results2, 
        current_time=current_time,
        custno=matno_value,
        custname=custname,
        user_name=user_name,
        user_level=user_level,
        photo_url=photo_url
    )