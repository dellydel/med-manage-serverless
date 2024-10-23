import boto3
import os
import uuid
from botocore.exceptions import ClientError
from src.http_response import create_response
from src.employees import save_employee_to_db

cognito_client = boto3.client('cognito-idp')
user_pool_id = os.environ.get('USER_POOL_ID')
client_id = os.environ.get('COGNITO_CLIENT_ID')
dynamodb = boto3.resource('dynamodb')

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
                {
                    'Name': 'custom:organizationId',
                    'Value': org_id, 
                },
            ],
            TemporaryPassword='TemporaryPassword123!',
            MessageAction='SUPPRESS'
        )

        cognito_client.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            GroupName=org_id,
            Username=username
        )

        save_employee_to_db(email, org_id, user_type, full_name)
        return create_response(200, "User created successfully.")
    
    except ClientError as e:
        print(f"Error creating user: {str(e)}")
        return create_response(500, "Failed to create new user.")

def login_user(email, password, domain):
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
            if 'AccessToken' in response['AuthenticationResult']:
                authentication_result = response['AuthenticationResult']
                access_token = authentication_result['AccessToken']
                id_token = authentication_result['IdToken']
                refresh_token = authentication_result['RefreshToken']
                
                secure = 'HttpOnly; Secure;' if domain != 'localhost:3000' else ''
                set_domain = domain if domain != 'localhost:3000' else 'localhost'

                cookies= [
                    f'access_token={access_token}; {secure} Path=/; Domain={set_domain}',
                    f'id_token={id_token}; {secure} Path=/; Domain={set_domain}',
                    f'refresh_token={refresh_token}; {secure} Path=/; Domain={set_domain}'
                ]
                
                return create_response(200, "Login was successful.", cookies)
            else: create_response(401, "Failed to authenticate.")
    
    except cognito_client.exceptions.NotAuthorizedException:
        # TODO: need to return appropriate response (invalid email, or email not confirmed)
        return create_response(401, 'Invalid email or password')
    except Exception as e:
        return create_response(500, str(e))

def update_user_password(email, new_password, session, domain):

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
        
        secure = 'HttpOnly; Secure;' if domain != 'localhost:3000' else ''
        set_domain = domain if domain != 'localhost:3000' else 'localhost'

        cookies= [
            f'access_token={access_token}; {secure} Path=/; Domain={set_domain}',
            f'id_token={id_token}; {secure} Path=/; Domain={set_domain}',
            f'refresh_token={refresh_token}; {secure} Path=/; Domain={set_domain}'
        ]
                
        return create_response(200, "Password update was successful.", cookies)

    else:
        create_response(401, "Failed to authenticate after new password update.")

def refresh_token(refresh_token, domain):
    try:
        response = cognito_client.admin_initiate_auth(
            UserPoolId=user_pool_id,  
            ClientId=client_id,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token
            }
        )

        if 'AccessToken' in response['AuthenticationResult']:
            authentication_result = response['AuthenticationResult']
            access_token = authentication_result['AccessToken']
            id_token = authentication_result['IdToken']
            
            secure = 'HttpOnly; Secure;' if domain != 'localhost:3000' else ''
            set_domain = domain if domain != 'localhost:3000' else 'localhost'

            cookies= [
                f'access_token={access_token}; {secure} Path=/; Domain={set_domain}',
                f'id_token={id_token}; {secure} Path=/; Domain={set_domain}',
                f'refresh_token={refresh_token}; {secure} Path=/; Domain={set_domain}'
            ]
                
            return create_response(200, "Login was successful.", cookies)
        
        else: create_response(401, "Failed to authenticate.")

    except cognito_client.exceptions.NotAuthorizedException:
        return create_response(401, "Invalid refresh token or the user is not authorized.")
    
    except Exception as e:
        return create_response(500, f"An error occurred: {str(e)}")

       