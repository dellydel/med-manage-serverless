import json
from src.http_response import create_response
from src.authorization import confirm_forgot_password

def handler(event, _):
    body = json.loads(event['body'])
    email = body.get('email')
    new_password = body.get('newPassword')
    confirmation_code = body.get('confirmationCode')

    if not email or not new_password:
        return create_response(400, 'Missing email or password')
    
    return confirm_forgot_password(email, new_password, confirmation_code)