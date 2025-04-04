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

# Get shipments with pagination and sorting (GET)
@app.route('/shipments', methods=['GET'])
@token_required
def get_shipments():
    shipment_id = request.args.get('shipment_id', None)
    page = request.args.get('page', 1, type=int)  
    per_page = request.args.get('per_page', 10, type=int)  # Default items per page is 10
    sort_by = request.args.get('sort_by', 'created_at')  # Default sort by created_at
    order = request.args.get('order', 'asc')  # Default order is ascending

    # Sorting logic
    if sort_by not in ['tracking_number', 'status', 'created_at']:
        return jsonify({'message': 'Invalid sort_by value. Use tracking_number, status, or created_at.'}), 400

    if order == 'desc':
        sort_column = getattr(Shipment, sort_by).desc()
    else:
        sort_column = getattr(Shipment, sort_by).asc()

    if shipment_id:
        shipment = Shipment.query.get(shipment_id)
        if shipment:
            shipment_data = {
                'shipment_id': shipment.id,
                'sender_name': shipment.sender_name,
                'sender_address': shipment.sender_address,
                'sender_phone': shipment.sender_phone,
                'receiver_name': shipment.receiver_name,
                'receiver_address': shipment.receiver_address,
                'receiver_phone': shipment.receiver_phone,
                'tracking_number': shipment.tracking_number,
                'service_type': shipment.service_type,
                'weight': shipment.weight,
                'description': shipment.description,
                'insurance_value': shipment.insurance_value,
                'cubic_measurement': shipment.cubic_measurement,
                'status': shipment.status,
                'number_of_items': shipment.number_of_items,
                'total_value': shipment.total_value,
                'total_gst': shipment.total_gst,
                'delivery_charges': shipment.delivery_charges,
                'created_at': shipment.created_at,
                'updated_at': shipment.updated_at
            }
            return jsonify(shipment_data), 200
        return jsonify({'message': 'Shipment not found'}), 404

    # Paginate and return all shipments if no specific id or tracking_number is provided
    shipments = Shipment.query.order_by(sort_column).paginate(page=page, per_page=per_page, error_out=False)
    shipment_list = []
    for shipment in shipments.items:
        shipment_data = {
            'shipment_id': shipment.id,
            'sender_name': shipment.sender_name,
            'sender_address': shipment.sender_address,
            'sender_phone': shipment.sender_phone,
            'receiver_name': shipment.receiver_name,
            'receiver_address': shipment.receiver_address,
            'receiver_phone': shipment.receiver_phone,
            'tracking_number': shipment.tracking_number,
            'service_type': shipment.service_type,
            'weight': shipment.weight,
            'description': shipment.description,
            'insurance_value': shipment.insurance_value,
            'cubic_measurement': shipment.cubic_measurement,
            'status': shipment.status,
            'number_of_items': shipment.number_of_items,
            'total_value': shipment.total_value,
            'total_gst': shipment.total_gst,
            'delivery_charges': shipment.delivery_charges,
            'created_at': shipment.created_at,
            'updated_at': shipment.updated_at
        }
        shipment_list.append(shipment_data)

    return jsonify({
        'shipments': shipment_list,
        'total_pages': shipments.pages,
        'current_page': shipments.page,
        'total_items': shipments.total
    }), 200


@app.route('/track', methods=['GET'])
def track_shipment():
    tracking_number = request.args.get('tracking_number', None)
    
    if not tracking_number:
        return jsonify({'message': 'Tracking number is required.'}), 400
    print(tracking_number,"tracking_number")

    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()
    
    if shipment:
        shipment_data = {
            'shipment_id': shipment.id,
            'sender_name': shipment.sender_name,
            'sender_address': shipment.sender_address,
            'sender_phone': shipment.sender_phone,
            'receiver_name': shipment.receiver_name,
            'receiver_address': shipment.receiver_address,
            'receiver_phone': shipment.receiver_phone,
            'tracking_number': shipment.tracking_number,
            'service_type': shipment.service_type,
            'weight': shipment.weight,
            'description': shipment.description,
            'insurance_value': shipment.insurance_value,
            'cubic_measurement': shipment.cubic_measurement,
            'status': shipment.status,
            'number_of_items': shipment.number_of_items,
            'total_value': shipment.total_value,
            'total_gst': shipment.total_gst,
            'delivery_charges': shipment.delivery_charges,
            'created_at': shipment.created_at,
            'updated_at': shipment.updated_at
        }
        return jsonify(shipment_data), 200
    return jsonify({'message': 'Shipment not found. Please check the tracking number and try again.'}), 404

# User Routes
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Check if the user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201

# Login User (POST)
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
