from flask import Blueprint, abort
from backend.compare.by_product import byproduct

compare_bp = Blueprint('compare', __name__)

@compare_bp.route('/by_product', methods=['GET', 'POST'])
def by_product():
    return byproduct()