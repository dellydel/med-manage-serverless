import os
import boto3
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('PATIENTS_TABLE'))

def get_all_patients(organization_id, active):
        response = table.scan(
            FilterExpression='organizationId = :orgId AND active = :active',
            ExpressionAttributeValues={
                ':orgId': organization_id,
                ':active': active
            }
        )
        if 'Items' in response:
            return response['Items']
        else:
            return None
    
def save_patient_to_db(body, org_id):

    first_name = body.get('firstName')
    last_name = body.get('lastName')
    email = body.get('email')
    phone = body.get('phone')
    street_address = body.get('streetAddress')
    city = body.get('city')
    zip_code = body.get('zipCode')
    state = body.get('state')
    contact_first_name = body.get('contactFirstName')
    contact_last_name = body.get('contactLastName')
    relationship = body.get('relationship')
    contact_phone = body.get('contactPhone')
    contact_street_address = body.get('contactStreetAddress')
    contact_city = body.get('contactCity')
    contact_zip_code = body.get('contactZipCode')
    contact_state = body.get('contactState')

    table.put_item(Item={
        'patientId' : str(uuid.uuid4()),
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'phone': phone,
        'streetAddress': street_address,
        'city': city,
        'zipCode': zip_code,
        'state': state,
        'contactFirstName': contact_first_name,
        'contactLastName': contact_last_name,
        'relationship': relationship,
        'contactPhone': contact_phone,
        'contactStreetAddress': contact_street_address,
        'contactCity': contact_city,
        'contactZipCode': contact_zip_code,
        'contactState': contact_state,
        'organizationId': org_id,
        'status': 'NEW',
        'active': True
    })

def update_patient_in_db(patient_id, body):
    first_name = body.get('firstName')
    last_name = body.get('lastName')
    email = body.get('email')
    phone = body.get('phone')
    street_address = body.get('streetAddress')
    city = body.get('city')
    zip_code = body.get('zipCode')
    state = body.get('state')
    contact_first_name = body.get('contactFirstName')
    contact_last_name = body.get('contactLastName')
    relationship = body.get('relationship')
    contact_phone = body.get('contactPhone')
    contact_street_address = body.get('contactStreetAddress')
    contact_city = body.get('contactCity')
    contact_zip_code = body.get('contactZipCode')
    contact_state = body.get('contactState')

    table.update_item(
        Key={
            'patientId': patient_id
        },
        UpdateExpression="""set #firstName = :firstName, #lastName = :lastName, #email = :email, #phone = :phone, #streetAddress = :streetAddress, #city = :city, #zipCode = :zipCode, #state = :state, #contactFirstName = :contactFirstName, #contactLastName = :contactLastName, #relationship = :relationship, #contactPhone = :contactPhone, #contactStreetAddress = :contactStreetAddress, #contactCity = :contactCity, #contactZipCode = :contactZipCode, #contactState = :contactState""",
        ExpressionAttributeNames={
            '#firstName': 'firstName',
            '#lastName': 'lastName',
            '#email': 'email',
            '#phone': 'phone',
            '#streetAddress': 'streetAddress',
            '#city': 'city',
            '#zipCode':'zipCode',
            '#state': 'state',
            '#contactFirstName':'contactFirstName',
            '#contactLastName': 'contactLastName',
            '#relationship':'relationship',
            '#contactPhone':'contactPhone',
            '#contactStreetAddress':'contactStreetAddress',
            '#contactCity':'contactCity',
            '#contactZipCode':'contactZipCode',
            '#contactState':'contactState'
        },
        ExpressionAttributeValues={
            ':firstName': first_name,
            ':lastName': last_name,
            ':email': email,
            ':phone': phone,
            ':streetAddress': street_address,
            ':city': city,
            ':zipCode': zip_code,
            ':state': state,
            ':contactFirstName': contact_first_name,
            ':contactLastName': contact_last_name,
            ':relationship': relationship,
            ':contactPhone': contact_phone,
            ':contactStreetAddress': contact_street_address,
            ':contactCity': contact_city,
            ':contactZipCode': contact_zip_code,
            ':contactState': contact_state,
            },
    )

def soft_delete_patient_in_db(patient_id):

    table.update_item(
        Key={
            'patientId': patient_id
        },
        UpdateExpression="set #active = :false", 
        ExpressionAttributeNames={
            '#active': 'active'
        },
        ExpressionAttributeValues={
            ':false': False
        }
    )