from src.employees import get_all_employees

def handler(event, _):
    #claims = event['requestContext']['authorizer']['claims']
    #organization_id = claims.get('custom:organization_id')
    #print(organization_id, "organization_id")
    #return get_all_employees(organization_id)
    return get_all_employees()