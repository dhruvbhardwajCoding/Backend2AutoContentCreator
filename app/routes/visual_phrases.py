from fastapi import APIRouter, HTTPException
from app.models.schemas import VisualPhrasesRequest, VisualPhrasesResponse
from app.services.visual_phrases import extract_visual_phrases

router = APIRouter()

@router.post("/extract-visual-phrases", response_model=VisualPhrasesResponse)
async def extract_phrases(request: VisualPhrasesRequest):
    try:
        result = extract_visual_phrases(request)
        return result
    except Exception as e:
        print(f"Visual Phrase Extraction Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract visual phrases.")
