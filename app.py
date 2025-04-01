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

if __name__ == '__main__':
    app.run(debug=True)
