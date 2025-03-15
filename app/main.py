from fastapi import FastAPI, HTTPException
from .schemas import GenerateRequest, GenerateResponse
import requests
import base64

app = FastAPI()

# URL Docker-container with Neural network
NEURAL_NET_URL = "http://localhost:8001/generate"  # port NN

@app.get("/")
def read_root():
    return {"status": "FastAPI works!"}

@app.post("/generate-image", response_model=GenerateResponse)
def generate_image(request: GenerateRequest):
    payload = {
        "prompt": request.prompt,
        "style": request.style,
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
