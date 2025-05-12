from flask import Blueprint, abort
from backend.top_sale.top_cust import topcust
from backend.top_sale.top_product import topproduct

top_sale_bp = Blueprint('top_sale', __name__)

@top_sale_bp.route('/top_cust', methods=['GET', 'POST'])
def top_cust():
    return topcust()

@top_sale_bp.route('/top_mat', methods=['GET', 'POST'])
def top_mat():
    return topproduct()