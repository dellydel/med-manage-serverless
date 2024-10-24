import json

from src.http_response import create_response
from src.authorization import refresh_token

def handler(event, _):
    body = json.loads(event['body'])
    token = body.get('refresh_token')

    if not token:
        return create_response(400, 'Missing refresh token')

    return refresh_token(token)
  