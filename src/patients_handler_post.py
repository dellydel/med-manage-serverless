import json
from src.http_response import create_response
from src.utils.token import get_token_from_event
from src.patients import save_patient_to_db
from botocore.exceptions import ClientError

def handler(event, _):
    try:

        token = get_token_from_event(event)
        organizationId = token.get("custom:organizationId")

        body = json.loads(event['body'])
        print(body)
        save_patient_to_db(body, organizationId)
        return create_response(200, "Patient record has been sucessfully created.")
    
    except KeyError as e:
            error_message = str(e)
            return create_response(500, f'You are not authorized to complete this action: {error_message}')
        
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Unable to add new patient record: {error_message}')
    
    except Exception as e:
        error_message = str(e)
        return create_response(500, f'Unable to add new patient record: {error_message}')