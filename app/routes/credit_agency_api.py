from flask import Blueprint, request, jsonify
from app.models.credit_agency import CreditAgency
from app import db
from datetime import datetime

credit_agency_api = Blueprint('credit_agency_api', __name__)

@credit_agency_api.route('/api/credit_agencies', methods=['GET'])
def get_all_credit_agencies():
    credits = CreditAgency.query.all()
    return jsonify([{
        'id': c.id,
        'employee_id': c.employee_id,
        'agency_name': c.agency_name,
        'credit_score': c.credit_score,
        'verification_status': c.verification_status,
        'verification_date': c.verification_date.strftime('%Y-%m-%d') if c.verification_date else None,
        'remarks': c.remarks
    } for c in credits])

@credit_agency_api.route('/api/credit_agencies/<int:credit_id>', methods=['GET'])
def get_credit_agency(credit_id):
    c = CreditAgency.query.get_or_404(credit_id)
    return jsonify({
        'id': c.id,
        'employee_id': c.employee_id,
        'agency_name': c.agency_name,
        'credit_score': c.credit_score,
        'verification_status': c.verification_status,
        'verification_date': c.verification_date.strftime('%Y-%m-%d') if c.verification_date else None,
        'remarks': c.remarks
    })

@credit_agency_api.route('/api/credit_agencies', methods=['POST'])
def create_credit_agency():
    data = request.get_json()
    required = ['employee_id', 'agency_name', 'credit_score', 'verification_status']
    if not all(field in data and data[field] for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    # Prevent duplicate credit agency for the same employee_id
    existing = CreditAgency.query.filter_by(employee_id=data['employee_id']).first()
    if existing:
        return jsonify({'error': 'A credit agency record for this employee already exists.'}), 400
    # Validate credit_score is between 0 and 999
    try:
        credit_score = int(data['credit_score'])
    except (ValueError, TypeError):
        return jsonify({'error': 'credit_score must be an integer'}), 400
    if not (0 <= credit_score <= 999):
        return jsonify({'error': 'credit_score must be between 0 and 999'}), 400
    credit = CreditAgency(
        employee_id=data['employee_id'],
        agency_name=data['agency_name'],
        credit_score=credit_score,
        verification_status=data['verification_status'],
        verification_date=datetime.strptime(data['verification_date'], '%Y-%m-%d') if data.get('verification_date') else None,
        remarks=data.get('remarks')
    )
    db.session.add(credit)
    db.session.commit()
    return jsonify({'message': 'Credit agency record created', 'id': credit.id}), 201

@credit_agency_api.route('/api/credit_agencies/<int:credit_id>', methods=['PUT'])
def update_credit_agency(credit_id):
    credit = CreditAgency.query.get_or_404(credit_id)
    data = request.get_json()
    if 'agency_name' in data:
        credit.agency_name = data['agency_name']
    if 'credit_score' in data:
        try:
            credit_score = int(data['credit_score'])
        except (ValueError, TypeError):
            return jsonify({'error': 'credit_score must be an integer'}), 400
        if not (0 <= credit_score <= 999):
            return jsonify({'error': 'credit_score must be between 0 and 999'}), 400
        credit.credit_score = credit_score
    if 'verification_status' in data:
        credit.verification_status = data['verification_status']
    if 'verification_date' in data:
        credit.verification_date = datetime.strptime(data['verification_date'], '%Y-%m-%d')
    if 'remarks' in data:
        credit.remarks = data['remarks']
    db.session.commit()
    return jsonify({'message': 'Credit agency record updated'})

@credit_agency_api.route('/api/credit_agencies/<int:credit_id>', methods=['DELETE'])
def delete_credit_agency(credit_id):
    credit = CreditAgency.query.get_or_404(credit_id)
    db.session.delete(credit)
    db.session.commit()
    return jsonify({'message': 'Credit agency record deleted'})
