from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Thread
from schemas import ThreadCreate, ThreadUpdate, ThreadList, ThreadInfo
from dependencies import get_current_user
from models import User

router = APIRouter(prefix="/threads", tags=["Threads"])

@router.post("/", response_model=ThreadInfo, status_code=status.HTTP_201_CREATED)
def create_thread(thread: ThreadCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_thread = Thread(
        title=thread.title,
        content=thread.content,
        user_id=current_user.id
    )
    db.add(new_thread)
    db.commit()
    db.refresh(new_thread)
    return new_thread

@router.get("/", response_model=List[ThreadList])
def list_threads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Thread).offset(skip).limit(limit).all()

@router.get("/{thread_id}", response_model=ThreadInfo)
def get_thread(thread_id: int, db: Session = Depends(get_db)):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread

@router.put("/{thread_id}", response_model=ThreadInfo)
def update_thread(thread_id: int, update: ThreadUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    if thread.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this thread")
    
    if update.title is not None:
        thread.title = update.title
    if update.content is not None:
        thread.content = update.content

    db.commit()
    db.refresh(thread)
    return thread

@router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_thread(thread_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    if thread.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this thread")

    db.delete(thread)
    db.commit()
    return
