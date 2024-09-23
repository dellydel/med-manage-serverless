import boto3
import os

from src.http_response import create_response

cognito_client = boto3.client('cognito-idp')
user_pool_id = os.environ.get('USER_POOL_ID')

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

def login_user(email, password):
    cognito_client = boto3.client('cognito-idp')
    
    try:
        response = cognito_client.initiate_auth(
            ClientId='5ml7sonmg6j630uaki7fkfaj06',
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        ) 

        if response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
           return create_response(200, {"session": response['Session'], "message": "Password Update Required"})

        else:
            access_token = response['AuthenticationResult']['AccessToken']
            id_token = response['AuthenticationResult']['IdToken']
            refresh_token = response['AuthenticationResult']['RefreshToken']
            
            return create_response(200, {
                'accessToken': access_token,
                'idToken': id_token,
                'refreshToken': refresh_token
            })
    
    except cognito_client.exceptions.NotAuthorizedException:
        return create_response(401, 'Invalid email or password')
    except Exception as e:
        return create_response(500, str(e))

def update_user_password(email, new_password, session):
    challenge_response = cognito_client.respond_to_auth_challenge(
        ClientId='5ml7sonmg6j630uaki7fkfaj06',
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

def logout_user():
   pass