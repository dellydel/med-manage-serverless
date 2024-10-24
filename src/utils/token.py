import jwt

def get_token_from_event(event):
    try:
        headers = event['headers']
        token = headers.get("Authorization")
        id_token = token.split(" ")[1]
        decodedToken = jwt.decode(id_token, algorithms=["RS256"], options={"verify_signature": False})
        return decodedToken
    
    except KeyError:
        raise KeyError("No token found in headers") 
