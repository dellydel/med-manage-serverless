import json
from src.http_response import create_response
from src.employees import update_employee_in_db
from botocore.exceptions import ClientError

def handler(event, _):

    body = json.loads(event['body'])
    employee_id = body.get('employeeId')

    if not employee_id:
        return create_response(400, "Employee ID is required.")

    try:
        update_employee_in_db(employee_id, body)
        return create_response(200, "Employee has been sucessfully updated.")

    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Unable to update employee: {error_message}')