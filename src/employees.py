import os
import boto3
import uuid
from botocore.exceptions import ClientError
from src.http_response import create_response

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = dynamodb.Table(os.environ.get('EMPLOYEES_TABLE'))

test_employees = [
    {
      "employeeType": "Clinician",
      "clinicianName": "PATRICIA EPIE",
      "clinicianEmailId": "epipat.pe@gmail.com",
      "assigned": 6,
      "onGoing": 1,
      "completed": 0,
      "reOpen": 0,
      "total": 7,
      "lastLogin": "17-May-2023 17:36:36",
    },
    {
      "employeeType": "Clinician",
      "clinicianName": "YUDI PATEL, PT",
      "clinicianEmailId": "rehabexpertsinc15@gmail.com",
      "assigned": 0,
      "onGoing": 1,
      "completed": 0,
      "reOpen": 0,
      "total": 1,
      "lastLogin": "28-Oct-2022 11:56:18",
    },
    {
      "employeeType": "Clinician",
      "clinicianName": "Fabian Ogala",
      "clinicianEmailId": "ogalaf@yahoo.com",
      "assigned": 0,
      "onGoing": 2,
      "completed": 2,
      "reOpen": 0,
      "total": 4,
      "lastLogin": "3-Feb-2023 17:48:22",
    },
    {
      "employeeType": "Clinician",
      "clinicianName": "Dionne Staten",
      "clinicianEmailId": "dionnestaten@yahoo.com",
      "assigned": 2,
      "onGoing": 2,
      "completed": 41,
      "reOpen": 1,
      "total": 46,
      "lastLogin": "25-Jul-2024 14:55:12",
    },
    {
      "employeeType": "Clinician",
      "clinicianName": "Demo Clinician",
      "clinicianEmailId": "demo@yahoo.com",
      "assigned": 0,
      "onGoing": 0,
      "completed": 0,
      "reOpen": 0,
      "total": 0,
      "lastLogin": "25-Jul-2024 14:55:12",
    },
    {
      "employeeType": "Clinician",
      "clinicianName": "Praise Udjue",
      "clinicianEmailId": "myworldofpraise.pu@gmail.com",
      "assigned": 1,
      "onGoing": 2,
      "completed": 7,
      "reOpen": 0,
      "total": 10,
      "lastLogin": "25-Jul-202414:48:24",
    }
  ]

def get_all_employees():
    try:
        response = table.scan()
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