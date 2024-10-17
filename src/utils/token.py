import jwt

def get_token_from_event(event):
    headers = event['headers']
    token = headers.get("Authorization")
    id_token = token.split(" ")[1]
    if not token:
        return None
    decodedToken = jwt.decode(id_token, algorithms=["RS256"], options={"verify_signature": False})
    return decodedToken