import boto3
import os
import uuid
import json 
from botocore.exceptions import ClientError
from src.http_response import create_response

cognito_client = boto3.client('cognito-idp')
user_pool_id = os.environ.get('USER_POOL_ID')
client_id = os.environ.get('COGNITO_CLIENT_ID')

def create_cognito_group(org_id, org_name):
    cognito_client.create_group(
        GroupName=org_id,
        UserPoolId=user_pool_id,
        Description=f'Group for organization: {org_name}'
    )

def create_admin_user(email, org_id):
    username=str(uuid.uuid4())

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

    cognito_client.admin_add_user_to_group(
        UserPoolId=user_pool_id,
        GroupName=org_id,
        Username=username
    )

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

def signup_new_user(full_name, email, org_id, user_type):
    # TODO: validate that user email does not already exist
    user_pool_id = os.environ.get('USER_POOL_ID')
    username = str(uuid.uuid4())
    
    try:
        cognito_client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'custom:full_name', 'Value': full_name},
                {'Name': 'custom:user_type', 'Value': user_type}    
            ],
            TemporaryPassword='TemporaryPassword123!',
            MessageAction='SUPPRESS'
        )

        cognito_client.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            GroupName=org_id,
            Username=username
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created successfully'})
        }
    except ClientError as e:
        print(f"Error creating user: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to create user'})
        }

def login_user(email, password):
    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            },
        ) 

        if response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
           return create_response(200, {"session": response['Session'], "message": "Password Update Required."})

        else:
            authentication_result = response['AuthenticationResult']
            access_token = authentication_result['AccessToken']
            id_token = authentication_result['IdToken']
            refresh_token = authentication_result['RefreshToken']
            return create_response(200, {
                'accessToken': access_token,
                'idToken': id_token,
                'refreshToken': refresh_token,
            })
    
    except cognito_client.exceptions.NotAuthorizedException:
        # TODO: need to return appropriate response (invalid email, or email not confirmed)
        return create_response(401, 'Invalid email or password')
    except Exception as e:
        return create_response(500, str(e))

def update_user_password(email, new_password, session):
    challenge_response = cognito_client.respond_to_auth_challenge(
        ClientId=client_id,
        ChallengeName='NEW_PASSWORD_REQUIRED',
        Session=session,
        ChallengeResponses={
            'USERNAME': email,
            'NEW_PASSWORD': new_password
        }
    )
   
    if 'AuthenticationResult' in challenge_response:
        access_token = challenge_response['AuthenticationResult']['AccessToken']
        id_token = challenge_response['AuthenticationResult']['IdToken']
        refresh_token = challenge_response['AuthenticationResult']['RefreshToken']
        
        return create_response(200, {
                'accessToken': access_token,
                'idToken': id_token,
                'refreshToken': refresh_token
        })
    else:
        create_response(401, "Failed to authenticate after new password update.")
