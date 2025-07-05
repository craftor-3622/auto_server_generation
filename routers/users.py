from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserInfo, UserUpdate
from models import User
from auth_utils import hash_password
from dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=UserInfo)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username exists")
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/account", response_model=UserInfo)
def get_account(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/account", response_model=UserInfo)
def update_account(update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if update.email:
        current_user.email = update.email
    if update.password:
        current_user.password = hash_password(update.password)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/account")
def delete_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"msg": "Account deleted"}
