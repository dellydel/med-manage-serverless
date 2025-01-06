from src.patients import get_all_patients
from src.employees import get_employee_by_id
from src.assignments import get_assignment 
from src.utils.token import get_token_from_event
from src.http_response import create_success_response, create_error_response
from botocore.exceptions import ClientError

def handler(event, _):
    query_params = event['queryStringParameters']
    active = True
    clinicianId = None
    if query_params:
        active_param = query_params.get("active", "true")
        active = active_param.lower() in ('true', '1') 
        clinicianId = query_params.get('clinicianId', None)
    try:
        token = get_token_from_event(event)
        organization_id = token.get("custom:organizationId")
        patients =  get_all_patients(organization_id, active)
        
        if not patients:
            return create_error_response(404, "No patients found.")
        else:
            for patient in patients:
                patient_id = patient.get('patientId')
                assignments = get_assignment(patient_id)
                if assignments and len(assignments) > 0:
                    employee = get_employee_by_id(assignments[0].get("employeeId"))
                    patient["clinicianAssigned"] = employee.get("fullName")
                    patient["clinicianId"] = assignments[0].get("employeeId")
                else:
                    patient["clinicianAssigned"] = None
                    patient["clinicianId"] = None
                    
            if clinicianId:
                patients = list(filter(lambda patient: patient.get("clinicianId") == clinicianId, patients))
            return create_success_response(patients)
    
    except KeyError as e:
        error_message = str(e)
        return create_error_response(500, f'You are not authorized to complete this action: {error_message}')
    
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_error_response(500, f'Unable to retrieve patients: {error_message}') 
    
    except Exception as e:
        return create_error_response(500, str(e))