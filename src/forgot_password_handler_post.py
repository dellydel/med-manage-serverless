import json
from src.http_response import create_error_response
from src.authorization import forgot_password

def handler(event, _):
    body = json.loads(event['body'])
    email = body.get('email')

    if not email:
        return create_error_response(400, 'Missing email.')
    
    return forgot_password(email)