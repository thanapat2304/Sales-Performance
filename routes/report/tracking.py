from flask import Blueprint, abort
from backend.login_funtions import login_required
from backend.tracking.lost_cust import lost_sale
from backend.tracking.lost_cust_detail import lost_detail
from backend.tracking.customer_tracking import customer_track, fetch_data
from backend.tracking.invoice_track import invoice_track
from backend.tracking.invoice_detail import detail_query
from backend.tracking.bill_welcome import bill_detail_py
from backend.tracking.summary_report import invoice_daily
from backend.pivot.summary_cus import summary_customer
from backend.pivot.summary_type import summary_type
from backend.pivot.summary_item import summary_item
from backend.pivot.summary_sale import summary_sale
from backend.pivot.history_price import history_price
from backend.main.total_cust import totalcust
from backend.tracking.new_total_cust import totalnew
from backend.tracking.lost_1_total_cust import totallost1
from backend.tracking.lost_2_total_cust import totallost2
from backend.tracking.lost_3_total_cust import totallost3
from backend.tracking.lost_6_total_cust import totallost6

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/lost')
@login_required
def lost():
    return lost_sale()

@tracking_bp.route('/lost_detail/<path:custno>')
@login_required
def lost_detail_py(custno):
    return lost_detail(custno)

@tracking_bp.route('/trackcus', methods=['GET', 'POST'])
@login_required
def trackcus():
    return customer_track()

@tracking_bp.route('/fetch-data', methods=['POST'])
@login_required
def fetch_tack():
    return fetch_data()

@tracking_bp.route('/trackinvo', methods=['GET', 'POST'])
@login_required
def trackinvo():
    return invoice_track()

@tracking_bp.route('/query')
@login_required
def detailquery():
    return detail_query()

@tracking_bp.route('/bill_welcome/<path:docno>')
@login_required
def bill_welcome(docno):
    return bill_detail_py(docno)

@tracking_bp.route('/dailyinvo', methods=['GET', 'POST'])
@login_required
def dailyinvo():
    return invoice_daily()

@tracking_bp.route('/summary_cus', methods=['GET', 'POST'])
@login_required
def summary_cus():
    return summary_customer()

@tracking_bp.route('/summary_ty', methods=['GET', 'POST'])
@login_required
def summary_ty():
    return summary_type()

@tracking_bp.route('/summary_it', methods=['GET', 'POST'])
@login_required
def summary_it():
    return summary_item()

@tracking_bp.route('/summary_sa', methods=['GET', 'POST'])
@login_required
def summary_sa():
    return summary_sale()

@tracking_bp.route('/histiry_pi', methods=['GET', 'POST'])
@login_required
def histiry_pi():
    return history_price()

@tracking_bp.route('/total_cust', methods=['GET', 'POST'])
@login_required
def total_cust():
    return totalcust()

@tracking_bp.route('/total_new')
@login_required
def total_new():
    return totalnew()

@tracking_bp.route('/total_lost1')
@login_required
def total_lost1():
    return totallost1()

@tracking_bp.route('/total_lost2')
@login_required
def total_lost2():
    return totallost2()


@tracking_bp.route('/total_lost3')
@login_required
def total_lost3():
    return totallost3()

@tracking_bp.route('/total_lost6')
@login_required
def total_lost6():
    return totallost6()