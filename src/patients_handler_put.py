import json
from src.http_response import create_response
from src.patients import update_patient_in_db

def handler(event, _):

    body = json.loads(event['body'])
    patient_id = body.get('patientId')

    if not patient_id:
        return create_response(400, "Patient ID is required.")

    update_patient_in_db(patient_id, body)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Patient record updated successfully.'})
    }