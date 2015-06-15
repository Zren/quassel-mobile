from flask import current_app, request
from flask.json import dumps

def jsonify(payload):
    # Equivalent to flask.jsonify() except the dict() wrapping the payload is removed.
    indent = None
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] and not request.is_xhr:
        indent = 2
    return current_app.response_class(dumps(payload, indent=indent), mimetype='application/json')
    