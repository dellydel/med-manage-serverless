import json
import jwt
from src.authorization import signup_new_user
from src.http_response import create_response

def handler(event, _):
    headers = event['headers']
    token = headers.get("Authorization")
    if not token:
        return create_response(401, "Unauthorized")
    decodedToken = jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})
    organizationId = decodedToken.get("custom:organizationId")

    body = json.loads(event['body'])
    email = body.get('email')
    user_type = body.get('user_type')
    full_name = body.get('full_name')
    return signup_new_user(full_name, email, organizationId, user_type)
