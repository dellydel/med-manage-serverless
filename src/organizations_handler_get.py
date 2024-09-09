from src.organizations import get_organization

def handler(event, _):
    query_params = event.get('queryStringParameters', {})
    orgId = query_params.get('orgId')
    return get_organization(orgId)
  