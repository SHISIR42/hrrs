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

@web_dbs_bp.route('/dbs/delete/<int:dbs_id>', methods=['POST', 'GET'])
def delete_dbs(dbs_id):
    dbs = DBS.query.get_or_404(dbs_id)
    employee_id = dbs.employee_id
    if request.method == 'POST':
        db.session.delete(dbs)
        db.session.commit()
        flash('DBS record deleted successfully!', 'success')
        return redirect(url_for('employee.employee_profile', id=employee_id))
    # For GET requests, just redirect to profile (or show a confirmation page if desired)
    return redirect(url_for('employee.employee_profile', id=employee_id))


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

# Update DBS route
@web_dbs_bp.route('/dbs/update/<int:dbs_id>', methods=['GET', 'POST'])
def update_dbs(dbs_id):
    dbs = DBS.query.get_or_404(dbs_id)
    if request.method == 'POST':
        # dbs.certificate_number = request.form.get('dbs_number')  # Do not update certificate number
        dbs.check_date = request.form.get('issue_date')
        dbs.status = request.form.get('status')
        dbs.remarks = request.form.get('remarks')
        db.session.commit()
        flash('DBS record updated successfully!', 'success')
        return redirect(url_for('employee.employee_profile', id=dbs.employee_id))
    return render_template('edit_dbs.html', dbs=dbs)
