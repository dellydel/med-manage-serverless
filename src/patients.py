import os
import boto3
import uuid
from botocore.exceptions import ClientError
from src.http_response import create_response

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('PATIENTS_TABLE'))

test_patients = [
    {
      "patientID": "CHCP1045",
      "patientName": "GERALD ARNORLD",
      "patientEmail": "epipat.pe@gmail.com",
      "clinicianAssignedId": "CHCC0008",
      "status": "IN PROGRESS",
    },
]

def get_all_patients(organization_id):
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
            return create_response(404, "Patients not found")
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Internal server error: {error_message}')
    
def save_patient_to_db(email, full_name, org_id):
    table.put_item(Item={
        'patientId' : str(uuid.uuid4()),
        'email': email,
        'organizationId': org_id,
        'fullName': full_name,
        'status': 'IN PROGRESS'
    })