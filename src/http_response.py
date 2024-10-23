import json

def create_response(status_code, body, headers=None):
  response = {
    "statusCode": status_code,
    "headers": {
      "Content-Type": "application/json",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE",
    },
    "body": body if isinstance(body, str) else json.dumps(body)
  }
  if headers:
    response['headers'].update(headers)