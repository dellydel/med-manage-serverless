import json
from src.authorization import signup_new_user

def handler(event, _):
    # TODO: get the org_id from the event instead of the body
    body = json.loads(event['body'])
    email = body.get('email')
    org_id = body.get('org_id')
    user_type = body.get('user_type')
    full_name = body.get('full_name')
    return signup_new_user(full_name, email, org_id, user_type)
