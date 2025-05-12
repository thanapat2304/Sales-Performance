from flask import Blueprint, abort
from backend.login_funtions import login_required
from backend.main.cust_ms import customer_master
from backend.main.cusms_detail import cusms_detail_py
from backend.main.stock import stock_master
from backend.main.stock_detail import stock_detail_py

main_bp = Blueprint('main', __name__)

@main_bp.route('/cust_ms', methods=['GET', 'POST'])
@login_required
def cust_ms():
    return customer_master()

@main_bp.route('/cusms_detal/<path:row1>', methods=['GET'])
@login_required
def cusms_detal(row1):
    if '+' in row1:
        row1_value, row10_value = row1.split('+')
    else:
        row1_value = row1
        row10_value = ""

    return cusms_detail_py(row1_value, row10_value)

@main_bp.route('/stock', methods=['GET', 'POST'])
@login_required
def stock():
    return stock_master()

@main_bp.route('/stock_detal/<path:row1>', methods=['GET'])
@login_required
def stock_detal(row1):
    if '+' in row1:
        row1_value, row8_value = row1.split('+')
    else:
        row1_value = row1
        row8_value = ""

    return stock_detail_py(row1_value, row8_value)