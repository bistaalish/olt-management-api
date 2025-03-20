from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models,oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import reseller

router = APIRouter(
    tags=["Resellers"],
    prefix = "/reseller"
)

'''
/reseller routes
'''
# GET /reseller
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowReseller])
def get_resellers(db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(oauth2.get_current_user)):
    if get_current_user.reseller_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return reseller.getAll(db)    
    


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowReseller)
def create(request: schemas.ResellerBase,db: Session= Depends(get_db),get_current_user:schemas.Reseller= Depends(oauth2.get_current_user)):
    # Create a new Reseller
   if get_current_user.reseller_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
   return reseller.create(request,db)

# GET /reseller/{reseller_id}
@router.get("/{reseller_id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowReseller)
def get_reseller(reseller_id: int, response: Response , db: Session = Depends(get_db),get_current_user:schemas.Reseller= Depends(oauth2.get_current_user)):
    if get_current_user.reseller_id != 1:
        if reseller_id == get_current_user.reseller_id:
            return reseller.getReseller(reseller_id,db)
        else:
            raise HTTPException(status_code=403, detail="Forbidden")
    return reseller.getReseller(reseller_id,db)


# DELETE /reseller/{reseller_id}
@router.delete("/{reseller_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reseller(reseller_id: int, db: Session = Depends(get_db),get_current_user:schemas.Reseller= Depends(oauth2.get_current_user)):
    if get_current_user.reseller_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return reseller.deleteReseller(reseller_id,db)

# PUT /reseller/{reseller_id}
@router.put("/{reseller_id}", status_code=status.HTTP_202_ACCEPTED)
def update_reseller(reseller_id: int, request: schemas.ResellerBase, db: Session = Depends(get_db),get_current_user:schemas.Reseller= Depends(oauth2.get_current_user)):
    if get_current_user.reseller_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return reseller.updateReseller(reseller_id,request,db)
