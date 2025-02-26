from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models
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
def get_resellers(db: Session = Depends(get_db)):
    return reseller.getAll(db)
    # resellers = db.query(models.Reseller).all()
    # if not resellers:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resellers found")
    # return resellers


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowReseller)
def create(request: schemas.ResellerBase,db: Session= Depends(get_db)):
    # Create a new Reseller
   return reseller.create(request,db)

# GET /reseller/{reseller_id}
@router.get("/{reseller_id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowReseller)
def get_reseller(reseller_id: int, response: Response , db: Session = Depends(get_db)):
    return reseller.getReseller(reseller_id,db)
    # reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    # if not reseller:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reseller with id {reseller_id} not found")
    # return reseller

# DELETE /reseller/{reseller_id}
@router.delete("/{reseller_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reseller(reseller_id: int, db: Session = Depends(get_db)):
    return reseller.deleteReseller(reseller_id,db)
    # if reseller_id == 1:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete the Admin reseller")
    # reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).delete(synchronize_session=False)
    # if not reseller:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reseller with id {reseller_id} not found")
    # db.commit()
    # return "deleted"  

# PUT /reseller/{reseller_id}
@router.put("/{reseller_id}", status_code=status.HTTP_202_ACCEPTED)
def update_reseller(reseller_id: int, request: schemas.ResellerBase, db: Session = Depends(get_db)):
    return reseller.updateReseller(reseller_id,request,db)
    # if reseller_id == 1:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update the Admin reseller")
    # reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    # if not reseller:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reseller with id {reseller_id} not found")
    # reseller.name = request.name
    # reseller.email = request.email
    # reseller.phone = request.phone
    # db.commit()
    # db.refresh(reseller)
    # return "updated"