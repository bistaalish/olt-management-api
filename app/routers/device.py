from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Devices"],
    prefix = "/device"
)

# GET /device
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowDevice])
def get_devices(db: Session = Depends(get_db)):
    devices = db.query(models.Device).all()
    if not devices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No devices found")
    return devices

# POST /device
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowDevice)
def create(request: schemas.Device,db: Session= Depends(get_db)):
    # Create a new Device
    device = db.query(models.Device).filter(models.Device.ip == request.ip).first()
    if device:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Device with this IP already exists")
    newDevice = models.Device(name=request.name,vendor=request.vendor,model=request.model,type=request.type,ip=request.ip,username=request.username,password=request.password,reseller_id=request.reseller_id)
    db.add(newDevice)
    db.commit()
    db.refresh(newDevice)
    return newDevice