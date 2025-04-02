from flask import Flask, request, jsonify,render_template
from models import db, Shipment, User
from config import Config
import random
import string
import jwt
import datetime
from utils import token_required

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize SQLite database
with app.app_context():
    db.create_all()

# Generating random tracking number
def generate_tracking_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Creating shipment (POST)
@app.route('/create_shipment', methods=['POST'])
@token_required
def create_shipment():
    data = request.get_json()

    sender_name = data['sender_name']
    sender_address = data['sender_address']
    sender_phone = data['sender_phone']
    receiver_name = data['receiver_name']
    receiver_address = data['receiver_address']
    receiver_phone = data['receiver_phone']
    service_type = data['service_type']
    weight = data['weight']
    description = data['description']
    insurance_value = data['insurance_value']
    cubic_measurement = data.get('cubic_measurement', None)
    status = data.get('status', 'pending')  # Default status is 'pending'
    number_of_items = data['number_of_items']
    total_value = data['total_value']
    total_gst = data['total_gst']
    delivery_charges = data['delivery_charges']
    
    # Generate a tracking number
    tracking_number = generate_tracking_number()
    
    # Create new shipment record
    new_shipment = Shipment(
        sender_name=sender_name,
        sender_address=sender_address,
        sender_phone=sender_phone,
        receiver_name=receiver_name,
        receiver_address=receiver_address,
        receiver_phone=receiver_phone,
        service_type=service_type,
        weight=weight,
        description=description,
        insurance_value=insurance_value,
        cubic_measurement=cubic_measurement,
        status=status,
        tracking_number=tracking_number,
        number_of_items=number_of_items,
        total_value=total_value,
        total_gst=total_gst,
        delivery_charges=delivery_charges
    )
    
    db.session.add(new_shipment)
    db.session.commit()
    
    return jsonify({'message': 'Shipment created successfully', 'shipment_id': new_shipment.id, 'tracking_number': tracking_number}), 201

# Updating shipment (PATCH)
@app.route('/update_shipment/<int:shipment_id>', methods=['PATCH'])
@token_required
def update_shipment(shipment_id):
    shipment = Shipment.query.get(shipment_id)
    
    if shipment:
        data = request.get_json()
        
        # Update the fields with the data provided in the request
        shipment.sender_name = data.get('sender_name', shipment.sender_name)
        shipment.sender_address = data.get('sender_address', shipment.sender_address)
        shipment.sender_phone = data.get('sender_phone', shipment.sender_phone)
        shipment.receiver_name = data.get('receiver_name', shipment.receiver_name)
        shipment.receiver_address = data.get('receiver_address', shipment.receiver_address)
        shipment.receiver_phone = data.get('receiver_phone', shipment.receiver_phone)
        shipment.service_type = data.get('service_type', shipment.service_type)
        shipment.weight = data.get('weight', shipment.weight)
        shipment.description = data.get('description', shipment.description)
        shipment.insurance_value = data.get('insurance_value', shipment.insurance_value)
        shipment.cubic_measurement = data.get('cubic_measurement', shipment.cubic_measurement)
        shipment.status = data.get('status', shipment.status)
        shipment.number_of_items = data.get('number_of_items', shipment.number_of_items)
        shipment.total_value = data.get('total_value', shipment.total_value)
        shipment.total_gst = data.get('total_gst', shipment.total_gst)
        shipment.delivery_charges = data.get('delivery_charges', shipment.delivery_charges)
        
        db.session.commit()
        
        return jsonify({'message': 'Shipment updated successfully'}), 200
    return jsonify({'message': 'Shipment not found'}), 404

# Deleting shipment (DELETE)
@app.route('/delete_shipment/<int:shipment_id>', methods=['DELETE'])
@token_required
def delete_shipment(shipment_id):
    shipment = Shipment.query.get(shipment_id)
    
    if shipment:
        db.session.delete(shipment)
        db.session.commit()
        return jsonify({'message': 'Shipment deleted successfully'}), 200
    return jsonify({'message': 'Shipment not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
