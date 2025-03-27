from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Shipment(db.Model):
    __tablename__ = 'shipments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Sender Information
    sender_name = db.Column(db.String(100), nullable=False)
    sender_address = db.Column(db.String(255), nullable=False)
    sender_phone = db.Column(db.String(50), nullable=False)
    
    # Receiver Information
    receiver_name = db.Column(db.String(100), nullable=False)
    receiver_address = db.Column(db.String(255), nullable=False)
    receiver_phone = db.Column(db.String(50), nullable=False)

    # Shipment Details
    service_type = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    insurance_value = db.Column(db.Float, nullable=False)
    cubic_measurement = db.Column(db.String(50), nullable=True)  

    status = db.Column(db.String(50), default="pending", nullable=False)
    tracking_number = db.Column(db.String(100), unique=True, nullable=False)  
    number_of_items = db.Column(db.Integer, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    total_gst = db.Column(db.Float, nullable=False)
    delivery_charges = db.Column(db.Float, nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=datetime.utcnow)  # Automatically updates on change

# Event listener to update the updated_at field on record updates
@event.listens_for(Shipment, 'before_update')
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.utcnow()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Store hashed password
    role = db.Column(db.String(50), default="user")  # Role: user or admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        """Hash the password before storing it"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the hashed password"""
        return check_password_hash(self.password_hash, password)