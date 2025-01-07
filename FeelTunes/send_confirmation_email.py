from itsdangerous import URLSafeTimedSerializer

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer("your_secret_key")  #  secret key
    return serializer.dumps(email, salt="email-confirmation-salt")

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer("your_secret_key")  #  secret key
    try:
        email = serializer.loads(token, salt="email-confirmation-salt", max_age=expiration)
    except Exception:
        return False
    return email


