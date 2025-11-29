from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .db import Base, engine, get_db
from . import models, schemas
from .jobs import enqueue_match_processing

# Auto-create tables on startup (dev only)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Football Highlight Backend")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/matches", response_model=schemas.MatchOut)
def create_match(match_in: schemas.MatchCreate, db: Session = Depends(get_db)):
    match = models.Match(
        title=match_in.title,
        video_url=match_in.video_url,
        status=models.MatchStatus.uploaded,
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


@app.post("/matches/{match_id}/process")
def process_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    if match.status == models.MatchStatus.processing:
        return {"detail": "Match is already processing"}

    match.status = models.MatchStatus.processing
    db.commit()

    job_id = enqueue_match_processing(match_id)
    return {"job_id": job_id, "match_id": match_id}


@app.get("/matches", response_model=List[schemas.MatchOut])
def list_matches(db: Session = Depends(get_db)):
    matches = db.query(models.Match).order_by(models.Match.id.desc()).all()
    return matches


@app.get("/matches/{match_id}", response_model=schemas.MatchDetail)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@app.get(
    "/matches/{match_id}/highlights",
    response_model=List[schemas.HighlightOut]
)
def get_highlights(match_id: int, db: Session = Depends(get_db)):
    highlights = (
        db.query(models.Highlight)
        .filter(models.Highlight.match_id == match_id)
        .order_by(models.Highlight.start_time)
        .all()
    )
    return highlights
