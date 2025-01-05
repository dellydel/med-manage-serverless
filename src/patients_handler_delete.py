from src.patients import soft_delete_patient_in_db
from botocore.exceptions import ClientError
from src.http_response import create_success_response, create_error_response

def handler(event, _):
    path_parameter = event['pathParameters']
    patient_id = path_parameter.get("patientId")

    try:
        soft_delete_patient_in_db(patient_id)
        return create_success_response("Patient has been successfully deleted.")

    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_error_response(500, f'Unable to delete patient: {error_message}')
