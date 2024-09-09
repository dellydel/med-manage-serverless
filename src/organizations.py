import os
import boto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from src.http_response import create_response

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = dynamodb.Table(os.environ.get('ORGANIZATIONS_TABLE'))

def get_organization(orgId):
    try:
        response = table.get_item(Key={'orgId': orgId})
        if 'Item' in response:
            return create_response(200, response['Item'])
        else:
            return create_response(404, "Organization not found")
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Internal server error: {error_message}')
