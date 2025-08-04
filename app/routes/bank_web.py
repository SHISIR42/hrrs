from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.employee import Employee
from app.models.bank import Bank
from app import db
from datetime import datetime

bank_web_bp = Blueprint('bank_web', __name__)

@bank_web_bp.route('/bank/list')
def list_banks():
    banks = Bank.query.all()
    return render_template('list_bank.html', banks=banks)
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.employee import Employee
from app.models.bank import Bank
from app import db
from datetime import datetime

bank_web_bp = Blueprint('bank_web', __name__)

@bank_web_bp.route('/bank/create', methods=['GET', 'POST'])
def create_bank():
    employees = Employee.query.all()
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        bank_name = request.form.get('bank_name')
        account_number = request.form.get('account_number')
        sort_code = request.form.get('sort_code')
        bic = request.form.get('bic')
        verification_status = request.form.get('verification_status')
        verification_date = request.form.get('verification_date')
        remarks = request.form.get('remarks')
        if not (employee_id and bank_name and sort_code and verification_status):
            flash('Please fill all required fields.', 'danger')
            return render_template('create_bank.html', employees=employees)
        bank_record = Bank(
            employee_id=employee_id,
            bank_name=bank_name,
            account_number=account_number,
            sort_code=sort_code,
            bic=bic,
            verification_status=verification_status,
            verification_date=datetime.strptime(verification_date, '%Y-%m-%d') if verification_date else None,
            remarks=remarks
        )
        db.session.add(bank_record)
        db.session.commit()
        flash('Bank details added successfully!', 'success')
        return redirect(url_for('bank_web.create_bank'))
    return render_template('create_bank.html', employees=employees)
