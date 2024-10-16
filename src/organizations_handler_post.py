import uuid
from datetime import datetime, timezone
import json
from src.organizations import create_organization
from src.authorization import create_cognito_group, create_admin_user, save_user_to_db
from src.http_response import create_response

def handler(event, _):
    body = json.loads(event['body'])
    org_id = str(uuid.uuid4())
    org_name = body.get('org_name')
    admin_name = body.get('admin_name')
    email = body.get('email')

    organization = {
        'organizationId': org_id,
        'createdAt': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
        'org_name': org_name,
        'admin_name': admin_name,
        'address': body.get('address'),
        'phone': body.get('phone'),
        'email': email, 
        'brandPrimary': body.get('brandPrimary'),
        'brandSecondary': body.get('brandSecondary'),
        'tagLine': body.get('tagLine'),
        'logoPath': body.get('logoPath'),
    }

    try:
        create_organization(organization)
        create_cognito_group(org_id, org_name)
        create_admin_user(email, org_id)
        save_user_to_db(email, org_id, "admin", admin_name)
        return create_response(200, f"Organization: '{org_name}' created successfully. Admin: {email}")
    except Exception as e:
        return create_response(500, f'Error creating organization: {e}')
