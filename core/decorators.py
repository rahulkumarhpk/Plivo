from fastapi import Request, HTTPException, status
from functools import wraps
from pydantic import ValidationError

# def jwt_required(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         request: Request = kwargs.get("request")
#         if request is None:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not found")

#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing or invalid")
        
#         token = auth_header.split(" ")[1]
        
#         from core.auth import JWTBearer
#         jwt_bearer = JWTBearer()
#         try:
#             payload = jwt_bearer.verify_jwt(token)
#             kwargs["user"] = payload
#         except HTTPException as e:
#             raise e
#         return await func(*args, **kwargs)
#     return wrapper

def validate_payload(schema_class):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if request is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not found")

            try:
                body = await request.json()
            except Exception:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid JSON")

            try:
                validated_data = schema_class(**body)
            except ValidationError as e:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())

            kwargs["validated_data"] = validated_data
            return await func(*args, **kwargs)
        return wrapper
    return decorator
