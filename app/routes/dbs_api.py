from flask import Blueprint, request, jsonify
from app.models.dbs import DBS
from app import db

dbs_api = Blueprint('dbs_api', __name__)

@dbs_api.route('/api/dbs', methods=['GET'])
def get_all_dbs():
    dbs_list = DBS.query.all()
    return jsonify([
        {
            'id': dbs.id,
            'employee_id': dbs.employee_id,
            'status': dbs.status,
            'check_date': dbs.check_date.isoformat() if dbs.check_date else None,
            'certificate_number': dbs.certificate_number,
            'remarks': dbs.remarks
        } for dbs in dbs_list
    ])

@dbs_api.route('/api/dbs', methods=['POST'])
def create_dbs():
    data = request.json
    # Prevent duplicate DBS for the same employee_id
    existing = DBS.query.filter_by(employee_id=data['employee_id']).first()
    if existing:
        return jsonify({'error': 'A DBS record for this employee already exists.'}), 400
    # Generate the next certificate number as a 12-digit string, starting from 0
    last_dbs = DBS.query.order_by(DBS.id.desc()).first()
    if last_dbs and last_dbs.certificate_number and last_dbs.certificate_number.isdigit():
        next_cert_num = int(last_dbs.certificate_number) + 1
    else:
        next_cert_num = 0
    cert_num_str = str(next_cert_num).zfill(12)
    dbs_record = DBS(
        employee_id=data['employee_id'],
        status=data['status'],
        check_date=data.get('check_date'),
        certificate_number=cert_num_str,
        remarks=data.get('remarks')
    )
    db.session.add(dbs_record)
    db.session.commit()
    return jsonify({'message': 'DBS record created', 'id': dbs_record.id, 'certificate_number': dbs_record.certificate_number}), 201

@dbs_api.route('/api/dbs/<int:id>', methods=['GET'])
def get_dbs(id):
    dbs = DBS.query.get_or_404(id)
    return jsonify({
        'id': dbs.id,
        'employee_id': dbs.employee_id,
        'status': dbs.status,
        'check_date': dbs.check_date.isoformat() if dbs.check_date else None,
        'certificate_number': dbs.certificate_number,
        'remarks': dbs.remarks
    })

@dbs_api.route('/api/dbs/<int:id>', methods=['PUT'])
def update_dbs(id):
    dbs = DBS.query.get_or_404(id)
    data = request.json
    dbs.employee_id = data['employee_id']
    dbs.status = data['status']
    dbs.check_date = data.get('check_date')
    # Only update certificate_number if provided
    if 'certificate_number' in data:
        dbs.certificate_number = data['certificate_number']
    dbs.remarks = data.get('remarks')
    db.session.commit()
    return jsonify({'message': 'DBS record updated'})

@dbs_api.route('/api/dbs/<int:id>', methods=['DELETE'])
def delete_dbs(id):
    dbs = DBS.query.get_or_404(id)
    db.session.delete(dbs)
    db.session.commit()
    return jsonify({'message': 'DBS record deleted'})
