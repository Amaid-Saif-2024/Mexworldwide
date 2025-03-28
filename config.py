import os

class Config:
    # SQLite database for local development
    SQLALCHEMY_DATABASE_URI = "sqlite:///shipment_db.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)