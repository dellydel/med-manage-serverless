from src.employees import soft_delete_employee_in_db
from botocore.exceptions import ClientError
from src.http_response import create_response

def handler(event, _):
    path_parameter = event['pathParameters']
    employee_id = path_parameter.get("employeeId")
    try:
        soft_delete_employee_in_db(employee_id)
        return create_response(200, "Employee has been successfully deleted.")
    
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Unable to delete employee: {error_message}')