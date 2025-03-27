from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models,oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import device,service,onudetails

router = APIRouter(
    tags=["ONU"],
    prefix = "/onu"
)

# GET /onu

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ONUOutput])
def get_onu(db: Session = Depends(get_db),get_current_user: schemas.Device = Depends(oauth2.get_current_user)):
    if get_current_user.reseller_id == 1:
        return onudetails.getAll(db)        
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

# GET /onu/{onu_id}