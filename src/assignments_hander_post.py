import json
from src.http_response import create_response
from src.utils.token import get_token_from_event
from botocore.exceptions import ClientError
from src.assignments import new_assignment

def handler(event, _):
    try:
        token = get_token_from_event(event)
        organizationId = token.get("custom:organizationId")

        body = json.loads(event['body'])
        employee_id = body.get('employeeId')
        patient_id = body.get('patientId')
    
        new_assignment(employee_id, patient_id, organizationId)
        return create_response(200, "New assignment has been sucessfully created.")

    except KeyError as e:
        error_message = str(e)
        return create_response(500, f'You are not authorized to complete this action: {error_message}')
    
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Unable to create new assignment: {error_message}')