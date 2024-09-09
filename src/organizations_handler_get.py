from src.organizations import get_organization

def handler(event, _):
    query_params = event.get('queryStringParameters', {})
    organizationId = query_params.get('organizationId')
    return get_organization(organizationId)
  