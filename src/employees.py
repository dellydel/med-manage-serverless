import os
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('EMPLOYEES_TABLE'))

def get_employee_by_id(employee_id):
    response = table.get_item(
        Key={'employeeId': employee_id})
    
    if 'Item' in response:
        return response['Item']
    else:
        return None

def get_all_employees(organization_id, type, active):
    
    filterExpression = 'organizationId = :orgId AND active = :active'
    expressionAttributeValues={
        ':orgId': organization_id,
        ':active': active
    }
    
    if type is not None:
        filterExpression += ' AND employeeType = :type'
        expressionAttributeValues[':type'] = type.capitalize()

    response = table.scan(
        FilterExpression=filterExpression,
        ExpressionAttributeValues=expressionAttributeValues
    )
    if 'Items' in response:
        return response['Items']
    else:
        return None
    
def save_employee_to_db(email, org_id, employee_type, full_name):
    table.put_item(Item={
        'employeeId' : str(uuid.uuid4()),
        'email': email,
        'organizationId': org_id,
        'employeeType': employee_type,
        'fullName': full_name,
        'active': True
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
