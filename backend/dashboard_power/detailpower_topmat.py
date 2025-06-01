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
    SELECT * FROM customers WHERE customer_id = 12345;
    """
    
    query2 = """
    SELECT * FROM customers WHERE customer_id = 12345;
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