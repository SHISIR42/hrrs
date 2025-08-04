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
    dbs_record = DBS(
        employee_id=data['employee_id'],
        status=data['status'],
        check_date=data.get('check_date'),
        certificate_number=data['certificate_number'],
        remarks=data.get('remarks')
    )
    db.session.add(dbs_record)
    db.session.commit()
    return jsonify({'message': 'DBS record created', 'id': dbs_record.id}), 201

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
