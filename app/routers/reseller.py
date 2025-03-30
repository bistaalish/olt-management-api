from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.exc import IntegrityError
from typing import List
from .. import schemas, models,oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import reseller
from ..middlewares import checkAdmin

router = APIRouter(
    tags=["Resellers"],
    prefix = "/reseller",
)


'''
/reseller routes
'''
# GET /reseller
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowReseller])
def get_resellers(db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(checkAdmin)):
    return reseller.getAll(db)    
    


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowReseller)
def create(request: schemas.ResellerBase,db: Session= Depends(get_db),get_current_user:schemas.Reseller = Depends(checkAdmin)):
    # Create a new Reseller
   if get_current_user.role_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
   return reseller.create(request,db)

# GET /reseller/{role_id}
@router.get("/{role_id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowReseller)
def get_reseller(role_id: int, response: Response , db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(checkAdmin)):
    if get_current_user.role_id != 1:
        if role_id == get_current_user.role_id:
            return reseller.getReseller(role_id,db)
        else:
            raise HTTPException(status_code=403, detail="Forbidden")
    return reseller.getReseller(role_id,db)


# DELETE /reseller/{role_id}
@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reseller(role_id: int, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(checkAdmin)):
    if get_current_user.role_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        # Attempt to delete the reseller
        return reseller.deleteReseller(role_id, db)
    except IntegrityError as e:
        # Handle foreign key constraint violation error
        db.rollback()  # Rollback the transaction
        raise HTTPException(status_code=400, detail="Cannot delete reseller due to foreign key constraints")
    except Exception as e:
        # For any other errors, raise a 500 server error
        if role_id == 1:
            raise HTTPException(status_code=400, detail="Cannot delete Admin reseller")
        db.rollback()  # Rollback the transaction in case of an unexpected error
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# PUT /reseller/{role_id}
@router.put("/{role_id}", status_code=status.HTTP_202_ACCEPTED,response_model=schemas.ShowReseller)
def update_reseller(role_id: int, request: schemas.ResellerBase, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(checkAdmin)):
    if get_current_user.role_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return reseller.updateReseller(role_id,request,db)
