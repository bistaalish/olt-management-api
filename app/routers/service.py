from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Services"],
    prefix = "/service"
)

# GET /service
@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowServiceProfile])
def get_services(db: Session = Depends(get_db)):
    services = db.query(models.ServiceProfile).all()
    if not services:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Services found")
    return services



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowServiceProfile)
def create(request: schemas.ServiceProfile, db: Session=Depends(get_db)):
    service = db.query(models.ServiceProfile).filter(models.ServiceProfile.vlan == request.vlan).first()
    if service:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service with this VLAN already exists")
    newService = models.ServiceProfile(name=request.name,serviceprofile_id=request.serviceprofile_id,lineprofile_id=request.lineprofile_id,gemport=request.gemport,vlan=request.vlan,device_id=request.device_id)
    db.add(newService)
    db.commit()
    db.refresh(newService)
    return newService
# GET /service/{id}
@router.get("/{id}",status_code=status.HTTP_400_BAD_REQUEST,response_model=schemas.ShowServiceProfile)
def get_service(id: int, db: Session = Depends(get_db)):
    service = db.query(models.ServiceProfile).filter(models.ServiceProfile.id == id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service

# PUT /service/{id}

@router.put("/{id}",status_code=status.HTTP_200_OK)
def update_service(id: int, request: schemas.ServiceProfile, db: Session = Depends(get_db)):
    service = db.query(models.ServiceProfile).filter(models.ServiceProfile.id == id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    service.name = request.name
    service.serviceprofile_id = request.serviceprofile_id
    service.lineprofile_id = request.lineprofile_id
    service.gemport = request.gemport
    service.vlan = request.vlan
    service.device_id = request.device_id
    db.commit()
    db.refresh(service)
    return "updated"

# DELETE /service/{id}

@router.delete("/{id}",status_code=status.HTTP_200_OK)
def delete_service(id: int, db: Session = Depends(get_db)):
    service = db.query(models.ServiceProfile).filter(models.ServiceProfile.id == id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    db.delete(service)
    db.refresh(service)
    db.commit()
    return "deleted"