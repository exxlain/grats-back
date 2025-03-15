from pydantic import BaseModel

class GenerateRequest(BaseModel):
    prompt: str          # text prompt
    n_prompt: str = "default"  # style of image optional

class GenerateResponse(BaseModel):
    image_base64: str    # result image in base64
