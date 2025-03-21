from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from ..database import SessionLocal, get_db
from .. import models,schemas

def getAll(db: Session = Depends(get_db)):
    services = db.query(models.ServiceProfile).all()
    if not services:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Services found")
    return services

    
def create(request: schemas.ServiceProfile, db: Session = Depends(get_db)):
    service = db.query(models.ServiceProfile).filter(models.ServiceProfile.vlan == request.vlan).first()
    if service:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service with this VLAN already exists")
    newService = models.ServiceProfile(name=request.name,serviceprofile_id=request.serviceprofile_id,lineprofile_id=request.lineprofile_id,gemport=request.gemport,vlan=request.vlan,device_id=request.device_id)
    db.add(newService)
    db.commit()
    db.refresh(newService)
    return newService

def getService(id: int, db: Session = Depends(get_db)):
    service = db.query(models.ServiceProfile).filter(models.ServiceProfile.id == id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service

def updateService(id: int, request: schemas.ServiceProfile, db: Session = Depends(get_db)):
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

def deleteService(id: int, db: Session = Depends(get_db)):
    service = db.query(models.ServiceProfile).filter(models.ServiceProfile.id == id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    db.delete(service)
    db.refresh(service)
    db.commit()
    return "deleted"

def getServicesByDevice(device_id: int, db: Session = Depends(get_db)):
    services = db.query(models.ServiceProfile).filter(models.ServiceProfile.device_id == device_id).all()
    if not services:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No services found for device with id {device_id}")
    return services