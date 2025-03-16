import jwt
import datetime
import secrets
import os
import logging
from dotenv import load_dotenv
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing in environment variables")
ALGORITHM = "HS256"

security = HTTPBearer()

def create_jwt_token(user_id: str, expires_in: int) -> str:
    """Generate JWT-token"""
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: HTTPAuthorizationCredentials = Depends(security)) -> str:
    logging.warning(f"Received Token: {token.credentials}")

    try:
        logging.warning(f"Using SECRET_KEY: {SECRET_KEY}")
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        logging.warning(f"Decoded Payload: {payload}")
        return payload["sub"]  # return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
