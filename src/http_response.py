import json

def create_response(status_code, body, mv_headers=None):
  response = {
    "statusCode": status_code,
    "headers": {
      "Content-Type": "application/json",
      "Access-Control-Allow-Headers": "Content-Type, Set-Cookie",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE",
      "Access-Control-Allow-Credentials": "true"
    },
    "body": body if isinstance(body, str) else json.dumps(body)
  }
  if mv_headers:
    response['multiValueHeaders'] = {"Set-Cookie": mv_headers}
  return response