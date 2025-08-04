from app import db


from datetime import datetime

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50))  # Optional
    sort_code = db.Column(db.String(20), nullable=False)
    bic = db.Column(db.String(20))  # Optional
    verification_status = db.Column(db.Enum('Verified', 'Pending', 'Failed', name='verification_status_enum'), nullable=False)
    verification_date = db.Column(db.DateTime, default=datetime.utcnow)
    remarks = db.Column(db.Text)

    employee = db.relationship('Employee', backref=db.backref('banks', cascade='all, delete-orphan'))
