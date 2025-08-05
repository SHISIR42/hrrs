from app import db

class CreditAgency(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False, unique=True)
    agency_name = db.Column(db.String(100), nullable=False)
    credit_score = db.Column(db.Integer, nullable=False)
    verification_status = db.Column(db.String(50), nullable=False)
    verification_date = db.Column(db.Date, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
