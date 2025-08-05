from app import db

class DBS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), unique=True)
    status = db.Column(db.String(50))
    check_date = db.Column(db.Date)
    certificate_number = db.Column(db.String(100))
    remarks = db.Column(db.Text)
