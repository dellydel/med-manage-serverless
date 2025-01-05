from src.employees import get_all_employees, get_employee_by_id
from src.utils.token import get_token_from_event
from src.http_response import create_success_response, create_error_response
from botocore.exceptions import ClientError

def handler(event, _):
    try:
        token = get_token_from_event(event)
        organization_id = token.get("custom:organizationId")
        query_params = event['queryStringParameters']
        active = True
        type = None
        employee_id = None
        if query_params:
            type = query_params.get("type", None)
            active_param = query_params.get("active", "true")
            active = active_param.lower() in ('true', '1') 
            employee_id = query_params.get("employeeId", None)
        if employee_id is not None:
            employee = get_employee_by_id(employee_id)
            if not employee:
                return create_error_response(404, "No employee found.")
            else:
                return create_success_response(employee)
                
        employees = get_all_employees(organization_id, type, active)
        if not employees:
            return create_error_response(404, "No employees found.")
        else:
            return create_success_response(employees)
            
    
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_error_response(500, f'Unable to retrieve employees: {error_message}')
    except Exception as e:
        return create_error_response(500, str(e))     