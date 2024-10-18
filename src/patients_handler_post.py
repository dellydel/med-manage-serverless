import json
from src.http_response import create_response
from src.utils.token import get_token_from_event
from src.patients import save_patient_to_db

def handler(event, _):
    token = get_token_from_event(event)
    if not token:
        return create_response(401, "Unauthorized")
    organizationId = token.get("custom:organizationId")

    body = json.loads(event['body'])
    email = body.get('email')
    full_name = body.get('fullName')

    save_patient_to_db(email, full_name, organizationId)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User created successfully'})
    }