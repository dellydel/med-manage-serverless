import json
from src.authorization import signup_new_user
from src.http_response import create_response
from src.utils.token import get_token_from_event
from botocore.exceptions import ClientError

def handler(event, _):
    try:
        token = get_token_from_event(event)
        organizationId = token.get("custom:organizationId")

        body = json.loads(event['body'])
        email = body.get('email')
        user_type = body.get('employeeType')
        full_name = body.get('fullName')
    
        signup_new_user(full_name, email, organizationId, user_type)
        return create_response(200, "Employee record has been sucessfully created.")

    except KeyError as e:
        error_message = str(e)
        return create_response(500, f'You are not authorized to complete this action: {error_message}')
    
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Unable to add new employee record: {error_message}')