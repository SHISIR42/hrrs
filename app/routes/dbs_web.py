from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.employee import Employee
from app.models.dbs import DBS
from app import db

# Blueprint for DBS web routes
web_dbs_bp = Blueprint('web_dbs', __name__)

def generate_certificate_number():
    last = DBS.query.order_by(DBS.id.desc()).first()
    if last and last.certificate_number and last.certificate_number.isdigit():
        next_num = int(last.certificate_number) + 1
    else:
        next_num = 1
    return str(next_num).zfill(12)

@web_dbs_bp.route('/dbs/create', methods=['GET', 'POST'])
def create_dbs():
    employees = Employee.query.all()
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        status = request.form.get('status')
        check_date = request.form.get('check_date')
        remarks = request.form.get('remarks')
        if not (employee_id and status and check_date):
            flash('All fields except remarks are required.', 'danger')
            return render_template('create_dbs.html', employees=employees)
        certificate_number = generate_certificate_number()
        dbs_record = DBS(
            employee_id=employee_id,
            status=status,
            check_date=check_date,
            certificate_number=certificate_number,
            remarks=remarks
        )
        db.session.add(dbs_record)
        db.session.commit()
        flash(f'DBS record created successfully! Certificate Number: {certificate_number}', 'dbs_create')
        return redirect(url_for('web_dbs.create_dbs'))
    return render_template('create_dbs.html', employees=employees)
