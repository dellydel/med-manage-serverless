from src.patients import get_all_patients
from src.assignments import get_assignment 
from src.utils.token import get_token_from_event
from src.http_response import create_response
from botocore.exceptions import ClientError

def handler(event, _):
    query_params = event['queryStringParameters']
    active = True
    if query_params:
        active_param = query_params.get("active", "true")
        active = active_param.lower() in ('true', '1') 
    try:
        token = get_token_from_event(event)
        organization_id = token.get("custom:organizationId")
        patients =  get_all_patients(organization_id, active)
        
        if patients is not None:
            for patient in patients:
                patient_id = patient.get('patientId')
                assignment = get_assignment(patient_id)
                patient["clinicianAssigned"] = assignment.get("employee_id")
            return create_response(200, patients)
        else:
            return create_response(404, "No patients found.")
    
    except KeyError as e:
        error_message = str(e)
        return create_response(500, f'You are not authorized to complete this action: {error_message}')
    
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Unable to retrieve patients: {error_message}') 