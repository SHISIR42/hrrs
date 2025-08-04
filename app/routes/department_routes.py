from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.employee import Department
from app import db

department_bp = Blueprint('department', __name__)

# List departments
@department_bp.route('/', methods=['GET'])
def list_departments():
    departments = Department.query.all()
    return render_template('list_department.html', departments=departments)

# Create department
@department_bp.route('/create', methods=['GET', 'POST'])
def create_department():
    if request.method == 'POST':
        name = request.form['name']
        if Department.query.filter_by(name=name).first():
            flash('Department already exists!', 'danger')
        else:
            dept = Department(name=name)
            db.session.add(dept)
            db.session.commit()
            flash('Department created!', 'success')
            return redirect(url_for('department.list_departments'))
    return render_template('create_department.html')

# Edit department
@department_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_department(id):
    dept = Department.query.get_or_404(id)
    if request.method == 'POST':
        new_name = request.form['name']
        dept.name = new_name
        db.session.commit()
        flash('Department updated!', 'success')
        return redirect(url_for('department.list_departments'))
    return render_template('edit_department.html', department=dept)

# Delete department
@department_bp.route('/delete/<int:id>', methods=['POST'])
def delete_department(id):
    dept = Department.query.get_or_404(id)
    db.session.delete(dept)
    db.session.commit()
    flash('Department deleted!', 'success')
    return redirect(url_for('department.list_departments'))
