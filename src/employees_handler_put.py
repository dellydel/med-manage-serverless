import json
from src.http_response import create_response
from src.employees import update_employee_in_db

def handler(event, _):

    body = json.loads(event['body'])
    employee_id = body.get('employeeId')

    if not employee_id:
        return create_response(400, "Employee ID is required.")

    update_employee_in_db(employee_id, body)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Employee record updated successfully.'})
    }