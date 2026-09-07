from fastapi import APIRouter, HTTPException
from app.models.schemas import GenerateRequest, GenerateResponse
from app.services.ai import generate_video_content

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
async def generate_content(request: GenerateRequest):
    try:
        result = generate_video_content(request)
        return result
    except Exception as e:
        # Log the actual error internally (omitted complex logging for brevity)
        print(f"AI Generation Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate content from AI backend.")
