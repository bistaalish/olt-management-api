from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .. import models,schemas
from ..hashing import Hash
from ..utils import Huawei

def getAll(db:Session):
    devices = db.query(models.Device).all()
    if not devices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No devices found")
    return devices

def create(request: schemas.Device, db: Session):
    device = db.query(models.Device).filter(models.Device.ip == request.ip).first()
    if device:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Device with this IP already exists")
    newDevice = models.Device(name=request.name,vendor=request.vendor,model=request.model,type=request.type,ip=request.ip,username=request.username,password=request.password,reseller_id=request.reseller_id)
    db.add(newDevice)
    db.commit()
    db.refresh(newDevice)
    return newDevice

def getDevice(device_id: int, db: Session):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Device with id {device_id} not found")
    return device

def deleteDevice(device_id: int, db: Session):
    device = db.query(models.Device).filter(models.Device.id == device_id).delete(synchronize_session=False)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Device with id {device_id} not found")
    db.commit()
    return "deleted"

def updateDevice(device_id: int, request: schemas.Device, db: Session):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Device with id {device_id} not found")
    device.name = request.name
    device.vendor = request.vendor
    device.model = request.model
    device.type = request.type
    device.ip = request.ip
    device.username = request.username
    device.password = request.password
    device.reseller_id = request.reseller_id
    db.commit()
    db.refresh(device)
    return device

def findONU(id: int,db:Session):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Device with id {id} not found")
    if device.vendor == "Huawei":
        tn = Huawei.TelnetSession(device)
        autofindResults = Huawei.autofind(tn)
        tn.close()
        # print(autofindResults["status"])
        if autofindResults["status"] == "failed":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ONU Found on Autofind")
    return autofindResults['devices']
    