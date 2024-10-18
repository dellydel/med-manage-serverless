from src.employees import get_all_employees
from src.utils.token import get_token_from_event
from src.http_response import create_response

def handler(event, _):
    query_params = event['queryStringParameters']
    type = None
    if query_params:
        type = query_params.get("type")
    token = get_token_from_event(event)
    if not token:
        return create_response(401, "Unauthorized")
    organization_id = token.get("custom:organizationId")
    return get_all_employees(organization_id, type)