from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, models, oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from ..token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..repository import device
from typing import List

router = APIRouter(

)

@router.post("/login",tags=['Authentication'])
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": user.email,  "roles" : user.roles.name}
    print("role:",data)
    access_token = create_access_token(
        data, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/dashboard",status_code=status.HTTP_200_OK,response_model=schemas.DashboardOutput, tags=['dashboard'])
def dashboard(db: Session = Depends(get_db),get_current_user:schemas.Device= Depends(oauth2.get_current_user)):
    if get_current_user.role_id == 1:
        deviceCount = db.query(models.Device).count()
        resellerCount = db.query(models.Reseller).count()
        ONUCount = db.query(models.ONUDetails).count()
        userCount = db.query(models.User).count()
        data = {
                "deviceCount": deviceCount,
                "resellerCount": resellerCount,
                "ONUCount": ONUCount,
                "userCount": userCount
            }
        return data
    # user = db.query(models.User).filter(models.User.email == get_current_user.email).first()
    # reseller = db.query(models.Reseller).filter(models.Reseller.id == get_current_user.reseller_id).first()
    # devices = device.getDeviceByResellerId(db,get_current_user.reseller_id)
    # data = {
    #     "user": user,
    #     "reseller": reseller,
    #     "devices":  devices
    # }
    # return data
