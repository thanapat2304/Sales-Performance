from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from backend.main_funtion import get_brand, get_year_compare
from decimal import Decimal
from datetime import datetime
from backend.main_funtion import get_profile_picture_url
import random

def byproduct():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    brands = get_brand()
    year = get_year_compare()
    photo_url = get_profile_picture_url()

    results = None
    selected_year = None
    selected_brand = None
    year_start = None
    year_end = None
    show_YR = None
    show_BR = None

    if request.method == 'POST':
        selected_year = request.form['YR']
        selected_brand = request.form['BR']
        show_YR = request.form.get('YR')
        show_BR = request.form.get('BR')

        year_start, year_end = selected_year.split('-')

        results = compare_ms(year_start, year_end, selected_brand)

    jan_growth = []
    feb_growth = []
    mar_growth = []
    apr_growth = []
    may_growth = []
    jun_growth = []
    jul_growth = []
    aug_growth = []
    sep_growth = []
    oct_growth = []
    nov_growth = []
    dec_growth = []

    if results:

        for row in results:
            values = [row[i] if row[i] is not None else 0 for i in range(3, 27)]
            values = [Decimal(v) if isinstance(v, str) else v for v in values]

            for i in range(0, len(values), 2):
                value_1 = values[i]
                value_2 = values[i+1]
        
                if value_1 == 0 or value_2 == 0:
                    if value_1 > 0:
                        growth = -100
                    elif value_2 > 0:
                        growth = 100
                    else:
                        growth = 'N/A'
                else:
                    growth = ((value_2 - value_1) / value_1) * 100
                    growth = round(growth, 2)

                if i == 0:
                    jan_growth.append(growth)
                elif i == 2:
                    feb_growth.append(growth)
                elif i == 4:
                    mar_growth.append(growth)
                elif i == 6:
                    apr_growth.append(growth)
                elif i == 8:
                    may_growth.append(growth)
                elif i == 10:
                    jun_growth.append(growth)
                elif i == 12:
                    jul_growth.append(growth)
                elif i == 14:
                    aug_growth.append(growth)
                elif i == 16:
                    sep_growth.append(growth)
                elif i == 18:
                    oct_growth.append(growth)
                elif i == 20:
                    nov_growth.append(growth)
                elif i == 22:
                    dec_growth.append(growth)

    return render_template('compare/by_product.html', brands=brands, year=year, results=results, year_start=year_start, year_end=year_end, user_level=user_level,
                       jan_growth=jan_growth, feb_growth=feb_growth, mar_growth=mar_growth, apr_growth=apr_growth, may_growth=may_growth, current_time=current_time,
                       jun_growth=jun_growth, jul_growth=jul_growth, aug_growth=aug_growth, sep_growth=sep_growth, user_name=user_name, photo_url=photo_url,
                       oct_growth=oct_growth, nov_growth=nov_growth, dec_growth=dec_growth, show_YR=show_YR, show_BR=show_BR, user_moduals=user_moduals)

def compare_ms(year_start, year_end, selected_brand):
    results = []
    
    for _ in range(10):
        row = [
            str(random.randint(1000, 9999)),
            f"Product {random.randint(1, 100)}",
            random.choice(['kg', 'ltr', 'pcs']),
            *[random.randint(0, 1000) for _ in range(24)]
        ]
        results.append(row)

    cleaned_results = [[col if col is not None else "0" for col in row] for row in results]

    return cleaned_results