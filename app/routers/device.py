from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import device
router = APIRouter(
    tags=["Devices"],
    prefix = "/device"
)

# GET /device
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.Device])
def get_devices(db: Session = Depends(get_db)):
    return device.getAll(db)


# POST /device
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.DeviceBase)
def create(request: schemas.DeviceBase,db: Session= Depends(get_db)):
    # Create a new Device
    return device.create(request,db)


# GET /device/{id}
@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=schemas.Device)
def get_device(id:int, db: Session = Depends(get_db)):
    return device.getDevice(id,db)


# PUT /device/{id}
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id:int,request: schemas.DeviceBase, db: Session = Depends(get_db)):
    return device.updateDevice(id,request,db)


# DELETE /device/{id}
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, db: Session = Depends(get_db)):
    return device.deleteDevice(id,db)
