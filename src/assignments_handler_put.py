import json
from src.http_response import create_response
from src.assignments import update_assignment
from botocore.exceptions import ClientError

def handler(event, _):

    body = json.loads(event['body'])
    employee_id = body.get('employeeId')
    assignment_id = body.get('assignmentId')

    if not employee_id or not assignment_id:
        return create_response(400, "Employee ID / Assignment ID are required.")

    try:
        update_assignment(assignment_id, employee_id)
        return create_response(200, "Assignment has been sucessfully updated.")

    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Unable to update assignment: {error_message}')