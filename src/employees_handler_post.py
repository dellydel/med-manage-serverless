import json
from src.authorization import signup_new_user
from src.http_response import create_response
from src.utils.token import get_token_from_event

def handler(event, _):
    token = get_token_from_event(event)
    if not token:
        return create_response(401, "Unauthorized")
    organizationId = token.get("custom:organizationId")

    body = json.loads(event['body'])
    email = body.get('email')
    user_type = body.get('userType')
    full_name = body.get('fullName')
    return signup_new_user(full_name, email, organizationId, user_type)
