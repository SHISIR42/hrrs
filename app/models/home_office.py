from app import db

class HomeOffice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    check_date = db.Column(db.Date, nullable=True)
    reference_number = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
