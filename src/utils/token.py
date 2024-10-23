import jwt

def get_token_from_event(event):
    try:
        id_token = get_cookie_value(event, 'id_token')
        decodedToken = jwt.decode(id_token, algorithms=["RS256"], options={"verify_signature": False})
        return decodedToken
    
    except KeyError:
        raise KeyError("No token found in headers") 
    
def get_cookie_value(event, cookie_name):
    cookies = event['headers'].get('Cookie', '')
    for cookie in cookies.split(';'):
        name, value = cookie.strip().split('=', 1)
        if name == cookie_name:
            return value
    return None
