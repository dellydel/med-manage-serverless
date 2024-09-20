import os
import boto3
from botocore.exceptions import ClientError
from src.http_response import create_response

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = dynamodb.Table(os.environ.get('ORGANIZATIONS_TABLE'))
cognito_client = boto3.client('cognito-idp')
user_pool_id = os.environ.get('USER_POOL_ID')

def get_organization(org_id):
    try:
        response = table.get_item(Key={'organizationId': org_id})
        if 'Item' in response:
            return create_response(200, response['Item'])
        else:
            return create_response(404, "Organization not found")
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return create_response(500, f'Internal server error: {error_message}')

def create_organization(organization):
    table.put_item(Item=organization)
    
def create_cognito_group(org_id, org_name):
    cognito_client.create_group(
        GroupName=org_id,
        UserPoolId=user_pool_id,
        Description=f'Group for organization: {org_name}'
    )

def create_cognito_user(username, email, org_id):
    cognito_client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username,
        UserAttributes=[
            {'Name': 'email', 'Value': email},
            {'Name': 'email_verified', 'Value': 'true'},
            {'Name': 'custom:organizationId', 'Value': org_id}
        ],
        TemporaryPassword='TemporaryPassword123!',
        MessageAction='SUPPRESS'
    )

def add_user_to_group(username, org_id):
    cognito_client.admin_add_user_to_group(
        GroupName=org_id,
        UserPoolId=user_pool_id,
        Username=username
    )

def update_user_org_id(username, org_id):
    cognito_client.admin_update_user_attributes(
        UserAttributes=[
            {
                'Name': 'custom:organizationId',
                'Value': org_id, 
            },
        ],
        UserPoolId=user_pool_id,
        Username=username
    )