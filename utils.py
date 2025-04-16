from functools import wraps
from flask import request, jsonify
import jwt
from models import User
from config import Config

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({
                'message': 'Authorization token is missing. Please include a valid token in the Authorization header, formatted as "Bearer <token>".'
            }), 403

        try:
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(decoded_token['user_id'])
            
            if not current_user:
                return jsonify({
                    'message': 'User associated with this token not found. Please ensure your token is valid.'
                }), 403

        except jwt.ExpiredSignatureError:

            return jsonify({
                'message': 'Token has expired. Please log in again to obtain a new token.'
            }), 403
        
        except jwt.InvalidTokenError:

            return jsonify({
                'message': 'Token is invalid. Please provide a valid token.'
            }), 403
        
        request.current_user = current_user
        return f(*args, **kwargs)

    return decorated_function
