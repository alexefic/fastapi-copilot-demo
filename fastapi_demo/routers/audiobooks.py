from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AudiobookDownload

router = APIRouter()

@router.post("/audiobooks/{audiobook_id}/download")
def download_audiobook(audiobook_id: int, db: Session = Depends(get_db)):
    # Logic to initiate download
    download = AudiobookDownload(audiobook_id=audiobook_id, user_id=1, progress=0, status="in_progress")  # Assuming user_id=1 for simplicity
    db.add(download)
    db.commit()
    return {"download_url": f"https://example.com/audiobooks/{audiobook_id}/download", "progress": 0}

@router.get("/audiobooks/{audiobook_id}/download/progress")
def get_download_progress(audiobook_id: int, db: Session = Depends(get_db)):
    download = db.query(AudiobookDownload).filter(AudiobookDownload.audiobook_id == audiobook_id, AudiobookDownload.user_id == 1).first()  # Assuming user_id=1 for simplicity
    if not download:
        raise HTTPException(status_code=404, detail="Download not found")
    return {"audiobook_id": audiobook_id, "progress": download.progress}
