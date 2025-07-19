from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def superuser_required():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("is_superuser"):
                return fn(*args, **kwargs)
            return jsonify({"msg": "Acesso restrito a superusuários"}), 403
        return wrapper
    return decorator
