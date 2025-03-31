from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.exc import IntegrityError
from typing import List
from .. import schemas, models,oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import reseller
from ..middlewares import checkAdmin, role_required

router = APIRouter(
    tags=["Resellers"],
    prefix = "/reseller",
)


'''
/reseller routes
'''
# GET /reseller
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowReseller])
def get_resellers(db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin"))):
    return reseller.getAll(db)    
    


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowReseller)
def create(request: schemas.ResellerBase,db: Session= Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin"))):
   return reseller.create(request,db)

# GET /reseller/{id}
@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowReseller)
def get_reseller(id: int, response: Response , db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin"))):
        return reseller.getReseller(id,db)


# DELETE /reseller/{id}
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reseller(id: int, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin"))):
    return reseller.deleteReseller(id, db)
    

# PUT /reseller/{id}
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED,response_model=schemas.ShowReseller)
def update_reseller(id: int, request: schemas.ResellerBase, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin"))):
    return reseller.updateReseller(id,request,db)
