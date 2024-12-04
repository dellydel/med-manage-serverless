from src.employees import get_all_employees, get_employee_by_id
from src.utils.token import get_token_from_event
from src.http_response import create_response
from botocore.exceptions import ClientError

def handler(event, _):
    token = get_token_from_event(event)
    organization_id = token.get("custom:organizationId")
    query_params = event['queryStringParameters']
    active = True
    type = None
    if query_params:
        type = query_params.get("type", None)
        active_param = query_params.get("active", "true")
        active = active_param.lower() in ('true', '1') 
        employee_id = query_params.get("employeeId", None)
    try:
        if employee_id is not None:
            employee = get_employee_by_id(employee_id)
            if employee is not None:
                return create_response(200, employee)
            else:
                return create_response(404, "No employee found.")
        employees = get_all_employees(organization_id, type, active)
        if employees is not None:
            return create_response(200, employees)
        else:
            return create_response(404, "No employees found.")
        
    except KeyError as e:
        error_message = str(e)
        return create_response(500, f'You are not authorized to complete this action: {error_message}')
    
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Unable to retrieve employees: {error_message}')     