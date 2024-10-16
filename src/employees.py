import os
import boto3
import uuid
from botocore.exceptions import ClientError
from src.http_response import create_response

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('EMPLOYEES_TABLE'))

def get_all_employees(organization_id):
    try:
        response = table.scan(
            FilterExpression='organizationId = :orgId',
            ExpressionAttributeValues={
              ':orgId': organization_id
            }
        )
        if 'Items' in response:
            return create_response(200, response['Items'])
        else:
            return create_response(404, "Employees not found")
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Internal server error: {error_message}')
    
def save_employee_to_db(email, org_id, employee_type, full_name):
    table.put_item(Item={
        'employeeId' : str(uuid.uuid4()),
        'email': email,
        'organizationId': org_id,
        'employeeType': employee_type,
        'fullName': full_name
    })