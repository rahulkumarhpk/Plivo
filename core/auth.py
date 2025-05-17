from fastapi.security import HTTPBearer
from fastapi import HTTPException, status
from jose import jwt
import requests
from core.config import settings

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    @staticmethod
    def verify_jwt(token: str):
        if settings.DEV_MODE and token == settings.TEST_TOKEN:
            return {
                "sub": "test_user",
                "email": "test@example.com",
                "permissions": ["all"]
            }
        try:
            jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
            jwks = requests.get(jwks_url).json()
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=settings.API_AUDIENCE,
                    issuer=f"https://{settings.AUTH0_DOMAIN}/"
                )
                return payload
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
