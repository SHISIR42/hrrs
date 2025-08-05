from flask import Blueprint, jsonify
from app.models.dbs import DBS
from app.models.home_office import HomeOffice
from app.models.bank import Bank
from app.models.credit_agency import CreditAgency

from app import db

compliance_api = Blueprint('compliance_api', __name__)

@compliance_api.route('/api/compliance_reports/<int:employee_id>', methods=['GET'])
def get_compliance_reports(employee_id):
    dbs_records = DBS.query.filter_by(employee_id=employee_id).all()
    home_office_records = HomeOffice.query.filter_by(employee_id=employee_id).all()
    bank_records = Bank.query.filter_by(employee_id=employee_id).all()
    credit_agency_records = CreditAgency.query.filter_by(employee_id=employee_id).all()

    dbs_list = [{
        'id': r.id,
        'employee_id': r.employee_id,
        'status': r.status,
        'check_date': r.check_date.strftime('%Y-%m-%d') if hasattr(r, 'check_date') and r.check_date else None,
        'certificate_number': getattr(r, 'certificate_number', None),
        'remarks': r.remarks
    } for r in dbs_records]

    home_office_list = [{
        'id': r.id,
        'employee_id': r.employee_id,
        'status': r.status,
        'check_date': r.check_date.strftime('%Y-%m-%d') if r.check_date else None,
        'reference_number': r.reference_number,
        'remarks': r.remarks
    } for r in home_office_records]

    bank_list = [{
        'id': r.id,
        'employee_id': r.employee_id,
        'bank_name': r.bank_name,
        'sort_code': r.sort_code,
        'bic': r.bic,
        'verification_status': r.verification_status,
        'verification_date': r.verification_date.isoformat() if r.verification_date else None,
        'account_number': r.account_number,
        'remarks': r.remarks
    } for r in bank_records]

    credit_agency_list = [{
        'id': r.id,
        'employee_id': r.employee_id,
        'agency_name': r.agency_name,
        'credit_score': r.credit_score,
        'verification_status': r.verification_status,
        'verification_date': r.verification_date.strftime('%Y-%m-%d') if r.verification_date else None,
        'remarks': r.remarks
    } for r in credit_agency_records]

    return jsonify({
        'dbs': dbs_list,
        'home_office': home_office_list,
        'bank': bank_list,
        'credit_agency': credit_agency_list
    })
