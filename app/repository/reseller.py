from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .. import models,schemas
from ..hashing import Hash



def getAll(db: Session):
    resellers = db.query(models.Reseller).all()
    if not resellers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resellers found")
    return resellers

def getResellerMe(reseller_id:int,db: Session):
    print(reseller_id)
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not reseller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reseller with id {reseller_id} not found")
    return reseller

def createReseller(data:dict,db:Session):
    reseller = db.query(models.Reseller).filter(models.Reseller.name == data['name']).first()
    if reseller:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reseller with this name already exists")
    newReseller = models.Reseller(name=data['name'],email=data['email'],phone=data['phone'])
    db.add(newReseller)
    db.commit()
    db.refresh(newReseller)
    return newReseller

def create(request: schemas.Reseller,db: Session):
    reseller = db.query(models.Reseller).filter(models.Reseller.name == request.name).first()
    if reseller:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reseller with this name already exists")
    newReseller = models.Reseller(
        name=request.name,
        Location=request.Location,
        Descriptions=request.Descriptions,
        phone=request.phone)
    db.add(newReseller)
    db.commit()
    db.refresh(newReseller)
    return newReseller

def getReseller(reseller_id: int, db: Session):
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not reseller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reseller with id {reseller_id} not found")
    return reseller

def deleteReseller(reseller_id: int, db: Session):
    # if reseller_id == 1:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete the Admin reseller") 
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).delete(synchronize_session=False)
    if not reseller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reseller with id {reseller_id} not found")
    db.commit()
    return "deleted"

def updateReseller(reseller_id: int, request: schemas.Reseller, db: Session):
    # if reseller_id == 1:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update the Admin reseller")
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not reseller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reseller with id {reseller_id} not found")
    reseller.name = request.name
    reseller.Location = request.Location
    reseller.Descriptions = request.Descriptions
    reseller.phone = request.phone
    db.commit()
    db.refresh(reseller)
    return reseller