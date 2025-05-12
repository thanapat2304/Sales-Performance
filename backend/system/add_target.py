from flask import render_template, session, request, jsonify
from backend.db_connection import connect_aep_portal, execute_query_portal
from datetime import datetime
from backend.main_funtion import get_profile_picture_url, get_salesman_all, get_years_up_down_one

def add_target():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    photo_url = get_profile_picture_url()
    salesman1, salesman2 = get_salesman_all()
    type_sale = get_type_sale()
    year = get_years_up_down_one()

    selected_salesman = None
    salesman_id = None
    salesman_name = None
    selected_typesale = None
    selected_year = None
    selected_January = None
    data_January = None
    selected_February = None
    data_February = None
    selected_March = None
    data_March = None
    selected_April = None
    data_April = None
    selected_May = None
    data_May = None
    selected_June = None
    data_June = None
    selected_July = None
    data_July = None
    selected_August = None
    data_August = None
    selected_September = None
    data_September = None
    selected_October = None
    data_October = None
    selected_November = None
    data_November = None
    selected_December = None
    data_December = None

    if request.method == 'POST':
        selected_salesman = request.form.get('salesman')
        salesman_id, salesman_name = selected_salesman.split(" | ")
        selected_typesale = request.form.get('typesale')
        if selected_typesale == 'Bangkok':
            selected_typesale = 'BKK'
        elif selected_typesale == 'Regional':
            selected_typesale = 'RG'
        selected_year = request.form.get('year')
        selected_January = request.form.get('January')
        data_January = float(selected_January.replace(',', '') if selected_January else 0)
        selected_February = request.form.get('February')
        data_February = float(selected_February.replace(',', '') if selected_February else 0)
        selected_March = request.form.get('March')
        data_March = float(selected_March.replace(',', '') if selected_March else 0)
        selected_April = request.form.get('April')
        data_April = float(selected_April.replace(',', '') if selected_April else 0)
        selected_May = request.form.get('May')
        data_May = float(selected_May.replace(',', '') if selected_May else 0)
        selected_June = request.form.get('June')
        data_June = float(selected_June.replace(',', '') if selected_June else 0)
        selected_July = request.form.get('July')
        data_July = float(selected_July.replace(',', '') if selected_July else 0)
        selected_August = request.form.get('August')
        data_August = float(selected_August.replace(',', '') if selected_August else 0)
        selected_September = request.form.get('September')
        data_September = float(selected_September.replace(',', '') if selected_September else 0)
        selected_October = request.form.get('October')
        data_October = float(selected_October.replace(',', '') if selected_October else 0)
        selected_November = request.form.get('November')
        data_November = float(selected_November.replace(',', '') if selected_November else 0)
        selected_December = request.form.get('December')
        data_December = float(selected_December.replace(',', '') if selected_December else 0)

        total_target = data_January + data_February + data_March + data_April + data_May + data_June + data_July + data_August + data_September + data_October + data_November + data_December

        if get_target_by_salesman(salesman_id, selected_year, selected_typesale):
            update_target(salesman_id, selected_typesale ,selected_year, data_January, data_February, data_March, data_April, data_May, data_June, data_July, data_August, data_September, data_October,
                          data_November, data_December, total_target)
        else:
            insert_target(salesman_id, selected_typesale, selected_year, salesman_name, data_January, data_February, data_March, data_April, data_May, data_June, data_July, data_August, data_September, 
                          data_October,data_November, data_December, total_target)

    return render_template('system/add_target.html', user_name=user_name, user_level=user_level, current_time=current_time, photo_url=photo_url, salesman1=salesman1,
                           salesman2=salesman2, type_sale=type_sale, year=year, user_moduals=user_moduals)

def get_type_sale():
    return [
        "Bangkok",
        "Regional"
    ]

def get_target_by_salesman(salesman_id, selected_year, selected_typesale):
    conn = connect_aep_portal()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rps_tb_target WHERE RPS_Target_id = %s AND RPS_Target_YR = %s AND RPS_Sales_Type = %s", (salesman_id, selected_year, selected_typesale,))
        exists = cursor.fetchone()[0] > 0
        cursor.close()
    finally:
        conn.close()
    return exists

def update_target(salesman_id, selected_typesale, selected_year, data_January, data_February, data_March, data_April, data_May, data_June, data_July, data_August, data_September, data_October, data_November, data_December, total_target):
    conn = connect_aep_portal()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE rps_tb_target 
        SET RPS_Jan = %s, RPS_Feb = %s, RPS_Mar = %s, RPS_Apr = %s, RPS_May = %s, RPS_Jun = %s, RPS_Jul = %s, RPS_Aug = %s, RPS_Sep = %s, RPS_Oct = %s, RPS_Nov = %s, RPS_Dec = %s, RPS_Target = %s
        WHERE RPS_Target_id = %s AND RPS_Target_YR = %s AND RPS_Sales_Type = %s
    """, (data_January, data_February, data_March, data_April, data_May, data_June, data_July, data_August, data_September, data_October, data_November, data_December, total_target, salesman_id, selected_year, selected_typesale))
    conn.commit()
    cursor.close()
    conn.close()

def insert_target(salesman_id, selected_typesale, selected_year, salesman_name, data_January, data_February, data_March, data_April, data_May, data_June, data_July, data_August, data_September, data_October, data_November, data_December, total_target):
    conn = connect_aep_portal()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rps_tb_target (RPS_Target_id, RPS_Sales_Type, RPS_Target_YR, RPS_Target_Name, RPS_Jan, RPS_Feb, RPS_Mar, RPS_Apr, RPS_May, RPS_Jun, RPS_Jul, RPS_Aug, RPS_Sep, RPS_Oct, RPS_Nov, RPS_Dec, RPS_Target)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (salesman_id, selected_typesale, selected_year, salesman_name, data_January, data_February, data_March, data_April, data_May, data_June, data_July, data_August, data_September, data_October, data_November, data_December, total_target))
    conn.commit()
    cursor.close()
    conn.close()

def get_lates_target(sales):
    if not sales:
        return jsonify({'error': 'Register parameter is missing'}), 400
    
    try:
        salesman_id, salesman_name = sales.split(" | ")
    except ValueError:
        return jsonify({'error': 'Invalid format for sales parameter'}), 400

    typesale = request.args.get('typesale')
    if typesale == 'Bangkok':
        typesale = 'BKK'
    elif typesale == 'Regional':
        typesale = 'RG'
    year = request.args.get('year')

    query = """
    SELECT RPS_Jan, RPS_Feb, RPS_Mar, RPS_Apr, RPS_May, RPS_Jun, RPS_Jul, RPS_Aug, RPS_Sep, RPS_Oct, RPS_Nov, RPS_Dec
    FROM rps_tb_target 
    WHERE RPS_Target_id = %s 
    AND RPS_Target_YR = %s
    AND RPS_Sales_Type = %s
    LIMIT 1
    """
    result = execute_query_portal(query, (salesman_id, year, typesale,))
    
    if result:
        return jsonify({
            'RPS_Jan': result[0]['RPS_Jan'],
            'RPS_Feb': result[0]['RPS_Feb'],
            'RPS_Mar': result[0]['RPS_Mar'],
            'RPS_Apr': result[0]['RPS_Apr'],
            'RPS_May': result[0]['RPS_May'],
            'RPS_Jun': result[0]['RPS_Jun'],
            'RPS_Jul': result[0]['RPS_Jul'],
            'RPS_Aug': result[0]['RPS_Aug'],
            'RPS_Sep': result[0]['RPS_Sep'],
            'RPS_Oct': result[0]['RPS_Oct'],
            'RPS_Nov': result[0]['RPS_Nov'],
            'RPS_Dec': result[0]['RPS_Dec']
        })
    else:
        return jsonify({
            'RPS_Jan': '',
            'RPS_Feb': '',
            'RPS_Mar': '',
            'RPS_Apr': '',
            'RPS_May': '',
            'RPS_Jun': '',
            'RPS_Jul': '',
            'RPS_Aug': '',
            'RPS_Sep': '',
            'RPS_Oct': '',
            'RPS_Nov': '',
            'RPS_Dec': ''})