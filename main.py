import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.routes.generate import router as generate_router

app = FastAPI(title="ReelSaaS AI Backend", version="1.0.0")

# Setup CORS (allowing all for local backend-to-backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Include routes
app.include_router(generate_router, tags=["Generate"])
from app.routes.visual_phrases import router as visual_phrases_router
app.include_router(visual_phrases_router, tags=["Visual Phrases"])

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
