import os
import boto3
from botocore.exceptions import ClientError
from src.http_response import create_response

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
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

def get_all_patients():
    try:
        # response = table.scan()
        return create_response(200, test_patients)
        # if 'Items' in response:
        #     return create_response(200, response['Items'])
        # else:
        #     return create_response(404, "Patients not found")
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Internal server error: {error_message}')