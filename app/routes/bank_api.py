from flask import Blueprint, request, jsonify
from app.models.bank import Bank
from app import db

bank_api = Blueprint('bank_api', __name__)

@bank_api.route('/api/bank', methods=['GET'])
def get_all_bank():
    records = Bank.query.all()
    return jsonify([{ 'id': r.id, 'employee_id': r.employee_id, 'status': r.verification_status, 'verification_date': r.verification_date.isoformat() if r.verification_date else None, 'account_number': r.account_number, 'remarks': r.remarks } for r in records])

@bank_api.route('/api/bank', methods=['POST'])
def create_bank():
    data = request.json
    required_fields = ['employee_id', 'verification_status', 'bank_name', 'sort_code']
    missing = [f for f in required_fields if f not in data or data.get(f) is None]
    if missing:
        return jsonify({'error': f'Missing required field(s): {", ".join(missing)}'}), 400
    record = Bank(
        employee_id=data['employee_id'],
        bank_name=data.get('bank_name'),
        sort_code=data.get('sort_code'),
        bic=data.get('bic'),
        verification_status=data.get('verification_status'),
        verification_date=data.get('verification_date'),
        account_number=data.get('account_number'),
        remarks=data.get('remarks')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Bank record created', 'id': record.id}), 201

@bank_api.route('/api/bank/<int:id>', methods=['GET'])
def get_bank(id):
    r = Bank.query.get_or_404(id)
    return jsonify({ 'id': r.id, 'employee_id': r.employee_id, 'status': r.verification_status, 'verification_date': r.verification_date.isoformat() if r.verification_date else None, 'account_number': r.account_number, 'remarks': r.remarks })

@bank_api.route('/api/bank/<int:id>', methods=['PUT'])
def update_bank(id):
    r = Bank.query.get_or_404(id)
    data = request.json
    required_fields = ['employee_id', 'verification_status', 'bank_name', 'sort_code']
    missing = [f for f in required_fields if f not in data or data.get(f) is None]
    if missing:
        return jsonify({'error': f'Missing required field(s): {", ".join(missing)}'}), 400
    r.employee_id = data['employee_id']
    r.bank_name = data.get('bank_name')
    r.sort_code = data.get('sort_code')
    r.bic = data.get('bic')
    r.verification_status = data.get('verification_status')
    r.verification_date = data.get('verification_date')
    r.account_number = data.get('account_number')
    r.remarks = data.get('remarks')
    db.session.commit()
    return jsonify({'message': 'Bank record updated'})

@bank_api.route('/api/bank/<int:id>', methods=['DELETE'])
def delete_bank(id):
    r = Bank.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Bank record deleted'})
