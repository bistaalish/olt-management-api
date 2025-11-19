from fastapi import APIRouter, Depends, status, Response, HTTPException, Query
from typing import List, Optional
from .. import schemas, models,oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import device,service,onudetails
from ..models import ONT

router = APIRouter(
    tags=["ONU"],
    prefix = "/onu"
)

# GET /onu

# @router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ONUOutput])
# def get_onu(db: Session = Depends(get_db),get_current_user: schemas.Device = Depends(oauth2.get_current_user)):
#     if get_current_user.reseller_id == 1:
#         return onudetails.getAll(db)        
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

# # GET /onu/{onu_id}


@router.get("/search", response_model=List[schemas.ONTBase])
def search_onu(
    query: Optional[str] = Query(None, description="Search by SN or description"),
    owner: Optional[str] = Query(None, description="Filter by owner: personal or gov"),
    db: Session = Depends(get_db)
):
    # Start with the base query
    q = db.query(models.ONT)

    # Filter by query if provided
    if query:
        q = q.filter(
            (models.ONT.SN.like(f"%{query}%")) | 
            (models.ONT.desc.like(f"%{query}%"))
        )

    # Filter by owner if provided
    if owner:
        q = q.filter(models.ONT.owner == owner)

    results = q.all()
    return results
