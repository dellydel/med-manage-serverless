import json
from src.http_response import create_response
from src.authorization import update_user_password

def handler(event, _):
    domain = event['headers'].get('Host', 'localhost')
    body = json.loads(event['body'])
    email = body.get('email')
    new_password = body.get('newPassword')
    session = body.get('session')

    if not email or not new_password:
        return create_response(400, 'Missing email or password')
    
    return update_user_password(email, new_password, session, domain)