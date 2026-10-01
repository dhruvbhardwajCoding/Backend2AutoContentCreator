from typing import List, Optional
from pydantic import BaseModel, Field

class TranscriptSegment(BaseModel):
    text: str
    start: float
    end: float
    confidence: float = 1.0

class GameplayEvent(BaseModel):
    type: str = Field(..., description="Event type: voice_reaction, audio_spike, kill, headshot, multi_kill, clutch")
    timestamp: float = Field(..., description="Event start time in seconds")
    endTimestamp: Optional[float] = Field(None, description="Event end time in seconds")
    importance: str = Field(default="low", description="low, medium, high, critical")
    source: str = Field(default="transcript", description="Detection source: transcript, audio_spike, vision, manual")
    label: Optional[str] = Field(None, description="Human-readable label for the event")

class MusicSlice(BaseModel):
    label: str = Field(..., description="Slice label: intro, climax, outro")
    musicStart: float = Field(..., description="Start time in the original music track")
    musicEnd: float = Field(..., description="End time in the original music track")
    duration: float
    type: str = Field(..., description="Section type: build, climax, resolve")
    energy: float = Field(default=0.5)

class MusicTimeline(BaseModel):
    trackId: str
    totalDuration: float
    slices: List[MusicSlice] = Field(default_factory=list)
    beats: List[float] = Field(default_factory=list, description="Beat timestamps relative to montage start")
    downbeats: List[float] = Field(default_factory=list, description="Downbeat timestamps relative to montage start")

class AnalyzeEditRequest(BaseModel):
    videoType: str = Field(..., description="One of: dance, yapping, gaming")
    transcript: List[TranscriptSegment] = Field(default_factory=list, description="Timestamped transcript segments (empty for dance)")
    duration: float = Field(..., description="Total video duration in seconds")
    intensity: str = Field(default="medium", description="Editing intensity: low, medium, high")
    gamingMode: Optional[str] = Field(None, description="For gaming: 'montage' or 'highlight'")
    gameplayEvents: List[GameplayEvent] = Field(default_factory=list, description="Detected gameplay events")
    musicTimeline: Optional[MusicTimeline] = Field(None, description="Music timeline for montage mode")

class EditSegment(BaseModel):
    start: float = Field(..., description="Segment start time in seconds")
    end: float = Field(..., description="Segment end time in seconds")
    type: str = Field(..., description="Semantic type: hook, important_statement, dead_air, filler, reaction, climax, transition, performance, no_edit")
    actions: List[str] = Field(default_factory=list, description="Recommended actions: caption, punch_in, zoom_out, sfx, trim, remove, preserve, slight_zoom")
    intensity: float = Field(default=0.5, description="How intensely to apply effects, 0.0 to 1.0")
    reason: str = Field(default="", description="Brief explanation for this editing decision")
    camera: Optional[str] = Field(None, description="Camera action: punch_in, punch_out, slide_left, slide_right, zoom_in, zoom_out")
    transition: Optional[str] = Field(None, description="Transition type: hard_cut, whip_left, whip_right, blur_transition, subtle_flash")
    gameplayClipStart: Optional[float] = Field(None, description="Source gameplay timestamp for this clip")
    gameplayClipEnd: Optional[float] = Field(None, description="Source gameplay end timestamp for this clip")
    beatSynced: Optional[bool] = Field(None, description="Whether this segment should sync to a music beat")

class AnalyzeEditResponse(BaseModel):
    segments: List[EditSegment] = Field(..., description="Ordered list of semantic editing segments covering the entire video duration")
    summary: str = Field(default="", description="Brief summary of the overall editing strategy")
