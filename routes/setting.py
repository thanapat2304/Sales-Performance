from flask import Blueprint
from backend.login_funtions import login_required
from backend.setting_user.profile import update_profile, upload_profile_picture

setting_bp = Blueprint('setting', __name__)

@setting_bp.route('/profile', methods=['GET', 'POST'], endpoint='update_profile')
@login_required
def profile():
    return update_profile()

@setting_bp.route('/upload_profile_picture', methods=['POST'])
def upload():
    return upload_profile_picture()