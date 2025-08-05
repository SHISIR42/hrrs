from flask import Blueprint, request, jsonify, abort
from app.models.home_office import HomeOffice
from app import db
from datetime import datetime

home_office_api = Blueprint('home_office_api', __name__)

@home_office_api.route('/api/home_offices', methods=['GET'])
def get_all_home_offices():
    records = HomeOffice.query.all()
    return jsonify([{
        'id': r.id,
        'employee_id': r.employee_id,
        'status': r.status,
        'check_date': r.check_date.strftime('%Y-%m-%d') if r.check_date else None,
        'reference_number': r.reference_number,
        'remarks': r.remarks
    } for r in records])

@home_office_api.route('/api/home_offices/<int:record_id>', methods=['GET'])
def get_home_office(record_id):
    r = HomeOffice.query.get_or_404(record_id)
    return jsonify({
        'id': r.id,
        'employee_id': r.employee_id,
        'status': r.status,
        'check_date': r.check_date.strftime('%Y-%m-%d') if r.check_date else None,
        'reference_number': r.reference_number,
        'remarks': r.remarks
    })

@home_office_api.route('/api/home_offices', methods=['POST'])
def create_home_office():
    data = request.get_json()
    required = ['employee_id', 'status', 'reference_number']
    if not all(field in data and data[field] for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    # Prevent duplicate home office record for the same employee_id
    existing = HomeOffice.query.filter_by(employee_id=data['employee_id']).first()
    if existing:
        return jsonify({'error': 'A home office record for this employee already exists.'}), 400
    record = HomeOffice(
        employee_id=data['employee_id'],
        status=data['status'],
        check_date=datetime.strptime(data['check_date'], '%Y-%m-%d') if data.get('check_date') else None,
        reference_number=data['reference_number'],
        remarks=data.get('remarks')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Home office record created', 'id': record.id}), 201

@home_office_api.route('/api/home_offices/<int:record_id>', methods=['PUT'])
def update_home_office(record_id):
    record = HomeOffice.query.get_or_404(record_id)
    data = request.get_json()
    if 'status' in data:
        record.status = data['status']
    if 'check_date' in data:
        record.check_date = datetime.strptime(data['check_date'], '%Y-%m-%d') if data['check_date'] else None
    if 'reference_number' in data:
        record.reference_number = data['reference_number']
    if 'remarks' in data:
        record.remarks = data['remarks']
    db.session.commit()
    return jsonify({'message': 'Home office record updated'})

@home_office_api.route('/api/home_offices/<int:record_id>', methods=['DELETE'])
def delete_home_office(record_id):
    record = HomeOffice.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Home office record deleted'})
