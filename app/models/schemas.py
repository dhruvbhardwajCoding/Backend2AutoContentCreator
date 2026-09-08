from typing import List, Optional
from pydantic import BaseModel, Field

class ChannelConfig(BaseModel):
    name: str = Field(..., description="The name of the channel")
    niche: str = Field(..., description="The niche or main topic of the channel")
    language: str = Field(default="en", description="The language of the content")
    duration: int = Field(default=30, description="Target duration of the video in seconds")
    description: Optional[str] = Field(None, description="Detailed instructions from the user on content style and focus")
    videosPerDay: int = Field(default=1, description="Number of videos generated per day")

class RecentVideo(BaseModel):
    topic: str
    script: Optional[str] = None
    createdAt: str

class GenerateRequest(BaseModel):
    channel: ChannelConfig
    recentVideos: List[RecentVideo] = Field(default_factory=list)

class GenerateResponse(BaseModel):
    topic: str = Field(..., description="A compelling, short topic for the next video")
    script: str = Field(..., description="The full, complete script for the video, optimized for spoken delivery and the requested duration. MUST be a complete sentence and not cut off.")

class VisualPhrasesRequest(BaseModel):
    topic: str = Field(..., description="The video topic")
    script: str = Field(..., description="The full video script")

class VisualPhrasesResponse(BaseModel):
    phrases: List[str] = Field(..., min_length=1, description="List of concise visual search phrases")
