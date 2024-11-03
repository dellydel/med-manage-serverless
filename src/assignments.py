import os
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('ASSIGNMENTS_TABLE'))

def get_assignment(patient_id):
    filterExpression = 'organizationId = :orgId'
    expressionAttributeValues={
        ':patientId': patient_id,
    }
    
    response = table.scan(
        FilterExpression=filterExpression,
        ExpressionAttributeValues=expressionAttributeValues
    )
    if 'Items' in response:
        return response['Items']
    else:
        return None

def new_assignment(employee_id, patient_id, org_id):
    table.put_item(Item={
        'assignmentId' : str(uuid.uuid4()),
        'employeeId': employee_id,
        'patientId': patient_id,
        'organizationId': org_id
    })

def update_assignment(assignment_id, employee_id):

    table.update_item(
        Key={
            'assignmentId': assignment_id
        },
        UpdateExpression="set #employeeId = :employee_id",
        ExpressionAttributeNames={
            '#employeeId': 'employeeId',
        },
        ExpressionAttributeValues={
            ':employee_id': employee_id,
        },
    )
    
