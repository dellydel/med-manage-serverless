import json
from src.http_response import create_success_response, create_error_response
from src.patients import update_patient_in_db
from botocore.exceptions import ClientError
def handler(event, _):

    body = json.loads(event['body'])
    patient_id = body.get('patientId')

    if not patient_id:
        return create_error_response(400, "Patient ID is required.")

    try:
        update_patient_in_db(patient_id, body)
        return create_success_response("Patient has been sucessfully updated.")

    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_error_response(500, f'Unable to update patient: {error_message}')
