from src.patients import get_all_patients
from src.utils.token import get_token_from_event
from src.http_response import create_response

def handler(event, _):
    token = get_token_from_event(event)
    if not token:
        return create_response(401, "Unauthorized")
    organization_id = token.get("custom:organizationId")
    return get_all_patients(organization_id)