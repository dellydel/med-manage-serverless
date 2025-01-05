import os
import boto3
from botocore.exceptions import ClientError
from src.http_response import create_success_response, create_error_response

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = dynamodb.Table(os.environ.get('ORGANIZATIONS_TABLE'))

def get_organization(org_id):
    try:
        response = table.get_item(Key={'organizationId': org_id})
        if 'Item' in response:
            return create_success_response(response['Item'])
        else:
            return create_error_response(404, "Organization not found")
    except ClientError as e:
        # TODO: Need to handle email already exists error
        error_message = e.response['Error']['Message']
        return create_error_response(500, f'Internal server error: {error_message}')

def create_organization(organization):
    table.put_item(Item=organization)