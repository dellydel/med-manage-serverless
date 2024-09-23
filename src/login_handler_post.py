import json

from src.http_response import create_response
from src.authorization import login_user

def handler(event, _):
    body = json.loads(event['body'])
    email = body.get('email')
    password = body.get('password')

    if not email or not password:
        return create_response(400, 'Missing email or password')
    
    return login_user(email, password)