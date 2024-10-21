import json
from src.employees import soft_delete_employee_in_db

def handler(event, _):
    path_parameter = event['pathParameters']
    employee_id = path_parameter.get("employeeId")
    soft_delete_employee_in_db(employee_id)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Patient record deleted successfully.'})
    }