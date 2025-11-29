import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# project-root imports; we'll run worker with PYTHONPATH set to repo root
from backend.app.db import Base  # noqa: F401
from backend.app import models

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://football:footballpassword@"
    "localhost:5432/football_highlights"
)

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def process_match(match_id: int):
    """
    Worker entrypoint for processing a football match.

    Currently:
    - Simulates processing with sleep
    - Creates a fake 'goal' highlight
    - Updates match status

    Later:
    - Load the video from match.video_url
    - Use PyAV to sample frames
    - Run MatchVision to classify events
    - Generate real highlight clips with ffmpeg
    """
    db = SessionLocal()
    try:
        match = (
            db.query(models.Match)
            .filter(models.Match.id == match_id)
            .first()
        )
        if not match:
            print(f"[worker] Match {match_id} not found")
            return

        print(f"[worker] Processing match {match.id}: {match.title}")

        # Simulate heavy processing
        time.sleep(5)

        # Stub: create a fake highlight
        fake_highlight = models.Highlight(
            match_id=match.id,
            start_time=120.0,
            end_time=135.0,
            event_type="goal",
            confidence=0.98,
            clip_url="s3://bucket/path/to/example_goal_clip.mp4",
        )

        db.add(fake_highlight)
        match.status = models.MatchStatus.done
        db.commit()

        print(f"[worker] Finished processing match {match.id}")

    except Exception as e:
        print(f"[worker] Error processing match {match_id}: {e}")
        match = (
            db.query(models.Match)
            .filter(models.Match.id == match_id)
            .first()
        )
        if match:
            match.status = models.MatchStatus.failed
            db.commit()
    finally:
        db.close()
