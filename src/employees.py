import os
import boto3
import uuid
from botocore.exceptions import ClientError
from src.http_response import create_response

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('EMPLOYEES_TABLE'))

def get_all_employees(organization_id, type):
    filterExpression = 'organizationId = :orgId AND active = :true'
    expressionAttributeValues={
        ':orgId': organization_id,
        ':true': True
    }
    
    if type is not None:
        filterExpression += ' AND employeeType = :type'
        expressionAttributeValues[':type'] = type.capitalize()
    try:
        response = table.scan(
            FilterExpression=filterExpression,
            ExpressionAttributeValues=expressionAttributeValues
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

def update_employee_in_db(employee_id, body):
    email = body.get('email')
    employee_type = body.get('employeeType')
    full_name = body.get('fullName')

    table.update_item(
        Key={
            'employeeId': employee_id
        },
        UpdateExpression="set #fullName = :full_name, #employeeType = :employee_type, #email = :email",
        ExpressionAttributeNames={
            '#email': 'email',
            '#fullName': 'fullName',
            '#employeeType': 'employeeType',
        },
        ExpressionAttributeValues={
            ':full_name': full_name,
            ':employee_type': employee_type,
            ':email': email,
            },
    )

def soft_delete_employee_in_db(employee_id):

    table.update_item(
        Key={
            'employeeId': employee_id
        },
        UpdateExpression="set #active = :false", 
        ExpressionAttributeNames={
            '#active': 'active'
        },
        ExpressionAttributeValues={
            ':false': False
        }
    )