from flask import Blueprint, request, redirect, url_for, jsonify
from backend.db_connection import connect_aep_portal
from backend.login_funtions import login_required
from backend.export_report.oneononesales import oneonone_sales, download_oneonone_sales
from backend.export_report.oneononebranch import oneonone_branch, download_oneonone_branch
from backend.export_report.Target_Actual import main_Target_Actual, download_Target_Actual
from backend.export_report.list_status import status_list

export_bp = Blueprint('export', __name__)

@export_bp.route('/sales_oneonone', methods=['GET', 'POST'])
@login_required
def sales_oneonone():
    return oneonone_sales()

@export_bp.route('/download_oneonone_sales')
@login_required
def download_sales_oneonone():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date') 
    return download_oneonone_sales(start_date, end_date)

@export_bp.route('/branch_oneonone', methods=['GET', 'POST'])
@login_required
def branch_oneonone():
    return oneonone_branch()

@export_bp.route('/download_oneonone_branch')
@login_required
def download_branch_oneonone():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date') 
    return download_oneonone_branch(start_date, end_date)

@export_bp.route('/target_actual', methods=['GET', 'POST'])
@login_required
def target_actual():
    return main_Target_Actual()

@export_bp.route('/download_Target_Actual')
@login_required
def download_Actual_Target():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date') 
    return download_Target_Actual(start_date, end_date)

@export_bp.route('/list_status', methods=['GET', 'POST'])
@login_required
def list_status():
    return status_list()

@export_bp.route('/delete_status/<int:id>', methods=['POST'])
def delete_record(id):
    conn = connect_aep_portal()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM tb_status_sales WHERE id_sales = %s", (id,))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        conn.close()
    return redirect(url_for('export.list_status'))

@export_bp.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    data = request.get_json()
    new_status = data['status']

    try:
        conn = connect_aep_portal()
        cursor = conn.cursor()

        cursor.execute('''UPDATE tb_status_sales SET REMARK_status = %s WHERE SMCODE_status = %s''', (new_status, id))
        
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'success': True})

    except Exception as e:
        print(f"Error updating status: {e}")
        return jsonify({'success': False}), 500