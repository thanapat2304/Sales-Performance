from flask import Flask, render_template, request, redirect, url_for, jsonify, session, abort, g
from datetime import timedelta, datetime
from backend.login_funtions import login , login_required
from backend.dashboard_user.dashboard import dashboard_sale, fetch_monthly, fetch_monthly_one, fetch_monthly_two
from backend.dashboard_user.two_dashboard import get_topic_data
from backend.dashboard_user.detail_topcust import purchase_detail
from backend.dashboard_power.dashboard_power import dashboard_two
from backend.dashboard_power.dashboard_detail import dash_detail, get_topic_data_sale, fetch_monthly_sale, fetch_monthly_one_sale, fetch_monthly_two_sale
from backend.dashboard_user.filltercust import show_results
from backend.dashboard_power.filltercust_power import power_results
from backend.dashboard_user.overview import sales_overview, fetch_monthly_over, fetch_monthly_one_over, fetch_monthly_two_over
from backend.dashboard_user.welcome import welcome_sale
from routes.report.tracking import tracking_bp
from routes.main.main_menu import main_bp
from backend.dashboard_user.detail_topmat import product_detail
from routes.setting import setting_bp
from backend.dashboard_power.detailpower_topmat import power_product_detail
from routes.system import system_bp
from backend.db_connection import connect_aep_portal
from routes.compare import compare_bp
from routes.top_sale import top_sale_bp
from routes.export import export_bp

app = Flask(__name__)
app.secret_key = '0000000000000000'
app.permanent_session_lifetime = timedelta(minutes=30)

app.register_blueprint(tracking_bp)
app.register_blueprint(main_bp)
app.register_blueprint(setting_bp)
app.register_blueprint(system_bp)
app.register_blueprint(compare_bp)
app.register_blueprint(top_sale_bp)
app.register_blueprint(export_bp)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('deadlock.html'), 500

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        return login()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard_user():
    return dashboard_sale()

@app.route('/get_monthly_data')
@login_required
def get_monthly_data():
    data_now = fetch_monthly()
    data_one = fetch_monthly_one()
    data_two = fetch_monthly_two()

    def convert_to_float(value):
        if value:
            return float(value.replace(',', '')) if isinstance(value, str) else value
        return None

    data_now = [{'month': item['month'], 'total_asset_value': convert_to_float(item['total_asset_value'])} for item in data_now]
    data_one = [{'month': item['month'], 'total_asset_value': convert_to_float(item['total_asset_value'])} for item in data_one]
    data_two = [{'month': item['month'], 'total_asset_value': convert_to_float(item['total_asset_value'])} for item in data_two]

    return jsonify({
        'now': [item['total_asset_value'] for item in data_now],
        'one_year': [item['total_asset_value'] for item in data_one],
        'two_year': [item['total_asset_value'] for item in data_two]
    })

@app.route('/purchase_detail/<path:custno>')
@login_required
def cust_detail(custno):
    return purchase_detail(custno)

@app.route('/matno_detail/<path:matno>')
@login_required
def mat_detail(matno):
    return product_detail(matno)

@app.route('/get-chart-data', methods=['GET'])
@login_required
def get_chart_data():
    data = get_topic_data()
    chart_data = {
        "labels": [row['End_Customer_Type'] for row in data],
        "series": [row['total_customers_no_sales'] for row in data]
    }
    return jsonify(chart_data)

@app.route('/dashboard_power')
@login_required
def dashboard_power():
    return dashboard_two()

@app.route('/sale_detail/<path:smcode>')
@login_required
def sale_detail(smcode):
    return dash_detail(smcode)

@app.route('/get-chart-data-sale/<smcode>', methods=['GET'])
@login_required
def get_chart_data_sale(smcode):
    data = get_topic_data_sale(smcode)
    chart_data = {
        "labels": [row['End_Customer_Type'] for row in data],
        "series": [row['total_customers_no_sales'] for row in data]
    }
    return jsonify(chart_data)

@app.route('/get_monthly_data_sale/<smcode>')
@login_required
def get_monthly_data_sale(smcode):
    data_now = fetch_monthly_sale(smcode)
    data_one = fetch_monthly_one_sale(smcode)
    data_two = fetch_monthly_two_sale(smcode)

    def convert_to_float(value):
        if value:
            return float(value.replace(',', '')) if isinstance(value, str) else value
        return None

    data_now = [{'month': item['month'], 'total_asset_value': convert_to_float(item['total_asset_value'])} for item in data_now]
    data_one = [{'month': item['month'], 'total_asset_value': convert_to_float(item['total_asset_value'])} for item in data_one]
    data_two = [{'month': item['month'], 'total_asset_value': convert_to_float(item['total_asset_value'])} for item in data_two]

    return jsonify({
        'now': [item['total_asset_value'] for item in data_now],
        'one_year': [item['total_asset_value'] for item in data_one],
        'two_year': [item['total_asset_value'] for item in data_two]
    })

@app.route('/results')
@login_required
def fillter_cust():
    return show_results()

@app.route("/power_results", methods=['GET', 'POST'])
@login_required
def fillter_power():
    return power_results()

@app.route("/power_matdetail/<path:matno_and_smcode>", methods=['GET'])
@login_required
def power_matdetail(matno_and_smcode):
    if '+' in matno_and_smcode:
        matno_value, smcode_value = matno_and_smcode.split('+')
    else:
        matno_value = matno_and_smcode
        smcode_value = ""

    return power_product_detail(matno_value, smcode_value)

@app.route('/overview_user')
@login_required
def overview_user():
    return sales_overview()

@app.route('/get_monthly_over')
@login_required
def get_monthly_data_over():

    data_now = fetch_monthly_over()
    data_one = fetch_monthly_one_over()
    data_two = fetch_monthly_two_over()

    data_now = [{'month': item['month'],'total_asset_value': float(item['total_asset_value']) if item['total_asset_value'] != '' else None}for item in data_now]
    data_one = [{'month': item['month'],'total_asset_value': float(item['total_asset_value']) if item['total_asset_value'] != '' else None}for item in data_one]
    data_two = [{'month': item['month'],'total_asset_value': float(item['total_asset_value']) if item['total_asset_value'] != '' else None}for item in data_two]

    return jsonify({
        'now': [item['total_asset_value'] for item in data_now],
        'one_year': [item['total_asset_value'] for item in data_one],
        'two_year': [item['total_asset_value'] for item in data_two]
    })

@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    return welcome_sale()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)