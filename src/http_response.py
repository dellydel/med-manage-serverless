import json

def create_response(status_code, body):
    return {
    "statusCode": status_code,
    "headers": {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE",
    },
    "body": body if isinstance(body, str) else json.dumps(body)
  }


