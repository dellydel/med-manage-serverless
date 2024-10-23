import json

def create_response(status_code, body):
    return {
    "statusCode": status_code,
    "headers": {
      "Content-Type": "application/json",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE",
    },
    "body": body if isinstance(body, str) else json.dumps(body)
  }

def create_response_set_cookies(
      access_token,
      id_token,
      refresh_token
    ):
    return {
    "statusCode": 200,
    "headers": {
      "Content-Type": "application/json",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE",
      "Set-Cookie": f"access_token={access_token}; HttpOnly; Secure; Path=/",
      "Set-Cookie": f"id_token={id_token}; HttpOnly; Secure; Path=/",
      "Set-Cookie": f"refresh_token={refresh_token}; HttpOnly; Secure; Path=/"
    },
    "body": "login successful"
  }