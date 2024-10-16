import jwt

def get_token_from_event(event):
    headers = event['headers']
    token = headers.get("Authorization")
    if not token:
        return None
    decodedToken = jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})
    return decodedToken