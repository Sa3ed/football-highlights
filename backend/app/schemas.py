from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class MatchStatus(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    done = "done"
    failed = "failed"


class HighlightBase(BaseModel):
    start_time: float
    end_time: float
    event_type: str
    confidence: Optional[float] = None
    clip_url: Optional[str] = None


class HighlightCreate(HighlightBase):
    pass


class HighlightOut(HighlightBase):
    id: int

    class Config:
        from_attributes = True


class MatchCreate(BaseModel):
    title: str
    video_url: str  # later this will be a stored URL/path


class MatchOut(BaseModel):
    id: int
    title: str
    video_url: str
    status: MatchStatus

    class Config:
        from_attributes = True


class MatchDetail(MatchOut):
    highlights: List[HighlightOut] = []