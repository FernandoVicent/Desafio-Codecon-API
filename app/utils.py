import time
from flask import jsonify
from functools import wraps
from datetime import datetime

def timed_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        duration = round((time.time() - start) * 1000, 2)
        timestamp = datetime.utcnow().isoformat()
        if isinstance(result, tuple):
            data, code = result
        else:
            data = result
            code = 200
        return jsonify({**data, "duration_ms": duration, "timestamp": timestamp}), code
    return wrapper
