from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from .db import Base


class MatchStatus(str, enum.Enum):
    uploaded = "uploaded"
    processing = "processing"
    done = "done"
    failed = "failed"


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    video_url = Column(String, nullable=False)
    status = Column(
        Enum(MatchStatus),
        default=MatchStatus.uploaded,
        nullable=False
    )

    highlights = relationship(
        "Highlight",
        back_populates="match",
        cascade="all, delete-orphan"
    )


class Highlight(Base):
    __tablename__ = "highlights"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)

    # Times in seconds from kick-off in the source video
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)

    # e.g. "goal", "shot_on_target", "save", "foul", "yellow_card"
    event_type = Column(String, nullable=False)

    confidence = Column(Float, nullable=True)
    clip_url = Column(String, nullable=True)

    match = relationship("Match", back_populates="highlights")