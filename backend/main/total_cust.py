from flask import render_template, session, request
from backend.db_connection import connect_aep_DB
from datetime import datetime, timedelta, date
from backend.main_funtion import get_profile_picture_url, get_years
import random

def totalcust():
    user_moduals = session.get('user_modual', '')
    user_name = session.get('user_name', None)
    user_level = session.get('user_level')
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    photo_url = get_profile_picture_url()
    year = get_years()

    results = None
    newlost = None
    selected_year = None
    year_show = None
    year_range = []
    two_year = []
    three_year = []

    start_year = None

    if request.method == 'POST':
        selected_year = request.form['year']
        year_show = request.form.get('year')

        start_year = int(selected_year)
        year_range = [str(start_year - 2), str(start_year - 1), str(start_year)]

        two_year = str(start_year - 1)
        three_year = str(start_year - 2)

    month_names = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    results = total(year_range, start_year, two_year, three_year)

    results_with_growth = []
    total_2022 = 0
    total_2023 = 0
    total_2024 = 0

    for i, row in enumerate(results):
        month = month_names[row[0]]
        year_2022 = row[1]
        year_2023 = row[2]
        year_2024 = row[3]

        growth_2023 = ((year_2023 - year_2022) / year_2022) * 100 if year_2022 != 0 else 0
        growth_2024 = ((year_2024 - year_2023) / year_2023) * 100 if year_2023 != 0 else 0

        total_2022 += year_2022
        total_2023 += year_2023
        total_2024 += year_2024
        
        results_with_growth.append((
            month,
            year_2022,
            round(growth_2023, 2),
            year_2023,
            round(growth_2024, 2),
            year_2024
        ))

    total_growth_2023 = ((total_2023 - total_2022) / total_2022) * 100 if total_2022 != 0 else 0
    total_growth_2024 = ((total_2024 - total_2023) / total_2023) * 100 if total_2023 != 0 else 0

    total_row = ("Total", total_2022, round(total_growth_2023, 2), total_2023, round(total_growth_2024, 2), total_2024)
    results_with_growth.append(total_row)

    newlost = count_new_lost(selected_year)

    return render_template('tracking/total_cust.html', results=results_with_growth, year_show=year_show, year=year, selected_year=selected_year, two_year=two_year, three_year=three_year, newlost=newlost,
                           user_name=user_name, user_level=user_level, current_time=current_time, photo_url=photo_url, user_moduals=user_moduals)

def total(year_range, start_year, two_year, three_year):
    if not year_range:
        return []

    data = []

    for month in range(1, 13):
        customer_count_three_year = random.randint(50, 200)
        customer_count_two_year = random.randint(50, 200)
        customer_count_start_year = random.randint(50, 200)

        data.append([
            month, 
            customer_count_three_year, 
            customer_count_two_year, 
            customer_count_start_year
        ])

    return data

def new_lost(selected_year):
    current_year = datetime.now().year
    current_month = datetime.now().month
    months_in_year = 12

    start_date = datetime(current_year - 1, 7, 1)
    end_date = datetime(current_year, 12, 31)

    data = []
    for _ in range(100):
        doc_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        cust_no = f'CUST{random.randint(1000, 9999)}'
        net_amount = round(random.uniform(1000, 10000), 2)
        data.append([doc_date, cust_no, net_amount])

    return data

def count_new_lost(selected_year):
    data = new_lost(selected_year)
    
    if not data:
        return None
    
    customers_by_year_month = {}

    for row in data:
        docdate = row[0]
        custno = row[1]
        
        year = docdate.year
        month = docdate.month
        
        if year not in customers_by_year_month:
            customers_by_year_month[year] = {m: set() for m in range(1, 13)}
        
        customers_by_year_month[year][month].add(custno)

    results = []
    
    for year in customers_by_year_month:
        months = range(1, 13)
        
        for i, current_month in enumerate(months):
            current_customers = customers_by_year_month[year][current_month]
            
            prev_customers = set()

            for months_ago7 in range(1, 7):
                prev_month7 = current_month - months_ago7
                prev_year7 = year
                if prev_month7 <= 0:
                    prev_month7 += 12
                    prev_year7 -= 1
                prev_customers.update(customers_by_year_month.get(prev_year7, {}).get(prev_month7, set())) #ลูกค้าในช่วง 7 เดือนก่อนฮะ
            
            new_customers = set()

            for row in data:
                docdate = row[0]
                custno = row[1]
                row_year = docdate.year
                row_month = docdate.month

                if row_year == year and row_month == current_month:
                    if custno not in prev_customers:
                        new_customers.add(custno)

            customers_4_months_ago = set()
            month_4_months_ago = current_month - 3
            year_4_months_ago = year
            if month_4_months_ago <= 0:
                month_4_months_ago += 12
                year_4_months_ago -= 1

            customers_4_months_ago = customers_by_year_month.get(year_4_months_ago, {}).get(month_4_months_ago, set()) #ลูกค้า 4 เดือนก่อนฮะ

            recent_customers = set()
            for months_ago4 in range(0, 3):
                prev_month4 = current_month - months_ago4
                prev_year4 = year
                if prev_month4 <= 0:
                    prev_month4 += 12
                    prev_year4 -= 1
                recent_customers.update(customers_by_year_month.get(prev_year4, {}).get(prev_month4, set())) #ลูกค้าในช่วง 4 เดือนก่อนฮะ

            lost_customers_three = customers_4_months_ago - recent_customers #ลูกค้าที่หายไป 3 เดือนฮะ

            customers_3_months_ago = set()
            month_3_months_ago = current_month - 2
            year_3_months_ago = year
            if month_3_months_ago <= 0:
                month_3_months_ago += 12
                year_3_months_ago -= 1

            customers_3_months_ago = customers_by_year_month.get(year_3_months_ago, {}).get(month_3_months_ago, set()) #ลูกค้า 3 เดือนก่อนฮะ

            recent_customers_two = set()
            for months_ago3 in range(0, 2):
                prev_month3 = current_month - months_ago3
                prev_year3 = year
                if prev_month3 <= 0:
                    prev_month3 += 12
                    prev_year3 -= 1
                recent_customers_two.update(customers_by_year_month.get(prev_year3, {}).get(prev_month3, set())) #ลูกค้าในช่วง 3 เดือนก่อนฮะ

            lost_customers_two = customers_3_months_ago - recent_customers_two #ลูกค้าที่หายไป 2 เดือนฮะ

            customers_2_months_ago = set()
            month_2_months_ago = current_month - 1
            year_2_months_ago = year
            if month_2_months_ago <= 0:
                month_2_months_ago += 12
                year_2_months_ago -= 1

            customers_2_months_ago = customers_by_year_month.get(year_2_months_ago, {}).get(month_2_months_ago, set()) #ลูกค้า 3 เดือนก่อนฮะ

            recent_customers_one = set()
            for months_ago2 in range(0, 1):
                prev_month2 = current_month - months_ago2
                prev_year2 = year
                if prev_month2 <= 0:
                    prev_month2 += 12
                    prev_year2 -= 1
                recent_customers_one.update(customers_by_year_month.get(prev_year2, {}).get(prev_month2, set())) #ลูกค้าในช่วง 2 เดือนก่อนฮะ

            lost_customers_one = customers_2_months_ago - recent_customers_one #ลูกค้าที่หายไป 1 เดือนฮะ

            customers_6_months_ago = set()
            month_6_months_ago = current_month - 6
            year_6_months_ago = year
            if month_6_months_ago <= 0:
                month_6_months_ago += 12
                year_6_months_ago -= 1

            customers_6_months_ago = customers_by_year_month.get(year_6_months_ago, {}).get(month_6_months_ago, set()) #ลูกค้า 6 เดือนก่อนฮะ

            recent_customers_six = set()
            for months_ago6 in range(0, 6):
                prev_month6 = current_month - months_ago6
                prev_year6 = year
                if prev_month6 <= 0:
                    prev_month6 += 12
                    prev_year6 -= 1
                recent_customers_six.update(customers_by_year_month.get(prev_year6, {}).get(prev_month6, set())) #ลูกค้าในช่วง 6 เดือนก่อนฮะ

            lost_customers_six = customers_6_months_ago - recent_customers_six #ลูกค้าที่หายไป 6 เดือนฮะ

            back_customers = set()
            for months_ago in range(1, 4):
                prev_month = current_month - months_ago
                prev_year = year
                if prev_month <= 0:
                    prev_month += 12
                    prev_year -= 1
                back_customers.update(customers_by_year_month.get(prev_year, {}).get(prev_month, set()))

            returned_customers = set()
            returned_customers = customers_4_months_ago - back_customers
            returned_customers = returned_customers & current_customers

            total_customers = len(current_customers)

            new_sales = sum(row[2] for row in data if row[0].year == year and row[0].month == current_month and row[1] in new_customers)

            total_total = sum(row[2] for row in data if row[0].year == year and row[0].month == (i + 1))

            lost_customers_one_sales = sum(row[2] for row in data if row[1] in lost_customers_one and row[0].year == year_2_months_ago and row[0].month == month_2_months_ago)

            lost_customers_two_sales = sum(row[2] for row in data if row[1] in lost_customers_two and row[0].year == year_3_months_ago and row[0].month == month_3_months_ago)

            lost_customers_three_sales = sum(row[2] for row in data if row[1] in lost_customers_three and row[0].year == year_4_months_ago and row[0].month == month_4_months_ago)

            lost_customers_six_sales = sum(row[2] for row in data if row[1] in lost_customers_six and row[0].year == year_6_months_ago and row[0].month == month_6_months_ago)

            net_cust_total = new_sales - lost_customers_six_sales
            
            results.append({
                "year": year,
                "month": current_month,
                "new": len(new_customers),
                "lost_one": len(lost_customers_one),
                "lost_two": len(lost_customers_two),
                "lost_three": len(lost_customers_three),
                "lost_six": len(lost_customers_six),
                "returning": len(returned_customers),
                "total": total_customers,
                "net_change": 0,
                "net_cust": len(new_customers) - len(lost_customers_six),
                "total_total": total_total,
                "new_sales": new_sales,
                "lost_one_sales": lost_customers_one_sales,
                "lost_two_sales": lost_customers_two_sales,
                "lost_three_sales": lost_customers_three_sales,
                "lost_six_sales": lost_customers_six_sales,
                "net_cust_total": net_cust_total
            })
    
    results = sorted(results, key=lambda x: x['year'])

    for i in range(1, len(results)):
        results[i]["net_change"] = results[i]["total"] - results[i-1]["total"]
    
    results = sorted(results, key=lambda x: x['year'])[12:]

    return results