from fastapi import FastAPI, HTTPException, Depends
from .auth import create_jwt_token, verify_jwt_token, decode_jwt_token
from .schemas import GenerateRequest, GenerateResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel
import requests
import base64
import os

class RefreshRequest(BaseModel):
    refresh_token: str

app = FastAPI()

security = HTTPBearer()

fake_users_db = {
    "test@example.com": "user123"
}


@app.post("/login")
def login(email: str):
    """user login, returned JWT-токен"""
    if email not in fake_users_db:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_jwt_token(fake_users_db[email], 900)  # 15 min
    refresh_token = create_jwt_token(fake_users_db[email], 604800)  # 7 days

    return {"access_token": access_token, "refresh_token": refresh_token}

@app.post("/refresh")
def refresh_token(request: RefreshRequest):
    """refresh access_token using refresh_token"""
    try:
        payload = decode_jwt_token(request.refresh_token)
        new_access_token = create_jwt_token(payload["sub"], 900)
        return {"access_token": new_access_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@app.get("/protected")
def protected_route(user_id=Depends(verify_jwt_token)):
    return {"message": "You are authenticated!", "user_id": user_id}



# URL Docker-container with Neural network
NEURAL_NET_URL = "http://localhost:8001/generate"  # port NN

@app.get("/")
def read_root():
    return {"status": "FastAPI works!"}

@app.post("/generate-image", response_model=GenerateResponse)
def generate_image(request: GenerateRequest):
    payload = {
        "prompt": request.prompt,
        "n_prompt": request.n_prompt,
    }

    try:
        response = requests.post(NEURAL_NET_URL, json=payload, timeout=60)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"net error: {str(e)}")

    data = response.json()

    if "image_base64" not in data:
        raise HTTPException(status_code=500, detail="NN didnt return image")

    return GenerateResponse(image_base64=data["image_base64"])
