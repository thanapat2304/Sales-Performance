from flask import Blueprint
from backend.login_funtions import login_required
from backend.system.target import target_sale
from backend.system.add_target import add_target
from backend.system.add_target import get_lates_target

system_bp = Blueprint('system', __name__)

@system_bp.route('/system')
@login_required
def system():
    return target_sale()

@system_bp.route('/add_target', methods=['GET', 'POST'])
@login_required
def addtarget():
    return add_target()

@system_bp.route('/get_lates_target/<sales>', methods=['GET'])
def latest_num_late(sales):
    return get_lates_target(sales)