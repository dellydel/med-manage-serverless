import json
from src.patients import soft_delete_patient_in_db

def handler(event, _):
    path_parameter = event['pathParameters']
    patient_id = path_parameter.get("patientId")
    soft_delete_patient_in_db(patient_id)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Patient record deleted successfully.'})
    }