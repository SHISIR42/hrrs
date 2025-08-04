from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models.employee import Employee, Department
from app import db

employee_bp = Blueprint('employee', __name__)

# API: Get all compliance records for an employee
from app.models.dbs import DBS
from app.models.home_office import HomeOffice
from app.models.bank import Bank
from app.models.credit_agency import CreditAgency

@employee_bp.route('/api/<int:id>/compliances', methods=['GET'])
def get_employee_compliances(id):
    dbs = [
        {'id': r.id, 'status': r.status, 'check_date': r.check_date.isoformat() if r.check_date else None, 'certificate_number': getattr(r, 'certificate_number', None), 'remarks': r.remarks}
        for r in DBS.query.filter_by(employee_id=id).all()
    ]
    home_office = [
        {'id': r.id, 'status': r.status, 'check_date': r.check_date.isoformat() if r.check_date else None, 'reference_number': r.reference_number, 'remarks': r.remarks}
        for r in HomeOffice.query.filter_by(employee_id=id).all()
    ]
    bank = [
        {'id': r.id, 'status': r.verification_status, 'check_date': r.verification_date.isoformat() if r.verification_date else None, 'account_number': r.account_number, 'remarks': r.remarks}
        for r in Bank.query.filter_by(employee_id=id).all()
    ]
    credit_agency = [
        {'id': r.id, 'status': r.status, 'check_date': r.check_date.isoformat() if r.check_date else None, 'reference_number': r.reference_number, 'remarks': r.remarks}
        for r in CreditAgency.query.filter_by(employee_id=id).all()
    ]
    return {
        'dbs': dbs,
        'home_office': home_office,
        'bank': bank,
        'credit_agency': credit_agency
    }

# API: Get employee by ID (for live search)
@employee_bp.route('/api/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    emp = Employee.query.get(id)
    if emp:
        return {'id': emp.id, 'name': emp.name}, 200
    else:
        return {'error': 'Employee not found'}, 404

# List employees - HTML page
@employee_bp.route('/', methods=['GET'])
def list_employees():
    employees = Employee.query.all()
    return render_template('list_employee.html', employees=employees)

# API endpoint - get all employees in JSON
@employee_bp.route('/api', methods=['GET'])
def get_employees_api():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])

# Create employee - form page (GET), save employee (POST)
@employee_bp.route('/create', methods=['GET', 'POST'])
def create_employee():
    departments = Department.query.all()
    if request.method == 'POST':
        data = request.form
        new_emp = Employee(
            name=data['name'],
            email=data['email'],
            ni_number=data['ni_number'],
            phone_number=data['phone_number'],
            address=data['address'],
            date_of_birth=data['date_of_birth'],
            department_id=data['department_id']
        )
        db.session.add(new_emp)
        db.session.commit()
        flash('Employee created successfully!', 'emp_create')
        return redirect(url_for('employee.create_employee'))
    return render_template('create_emp.html', departments=departments)

# Delete employee (POST)
@employee_bp.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    emp = Employee.query.get_or_404(id)
    # Delete all related compliance records
    DBS.query.filter_by(employee_id=emp.id).delete()
    HomeOffice.query.filter_by(employee_id=emp.id).delete()
    Bank.query.filter_by(employee_id=emp.id).delete()
    CreditAgency.query.filter_by(employee_id=emp.id).delete()
    db.session.delete(emp)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('employee.list_employees'))

# Update employee - form page and update logic
@employee_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    emp = Employee.query.get_or_404(id)
    departments = Department.query.all()
    if request.method == 'POST':
        data = request.form
        emp.name = data['name']
        emp.email = data['email']
        emp.ni_number = data['ni_number']
        emp.phone_number = data['phone_number']
        emp.address = data['address']
        emp.date_of_birth = data['date_of_birth']
        emp.department_id = data['department_id']
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('employee.list_employees'))
    return render_template('edit_employee.html', employee=emp, departments=departments)

# Employee profile - HTML page
@employee_bp.route('/profile/<int:id>', methods=['GET'])
def employee_profile(id):
    emp = Employee.query.get_or_404(id)
    return render_template('employee_profile.html', employee=emp)
