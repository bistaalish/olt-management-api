from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, models
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from ..JWTtoken import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    tags=["Authentication"],
)

@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
