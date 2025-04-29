from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models,oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import device,service,onudetails,user
from ..middlewares import checkAdmin, role_required

router = APIRouter(
    tags=["Devices"],
    prefix = "/device"
)

# GET /device
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowDevice])
def get_devices(db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    if get_current_user.roles == "Admin":
        return device.getAll(db)
    else:
        user = db.query(models.User).filter(models.User.email == get_current_user.email).first()
        return device.getDeviceByResellerId(db,user.reseller_id)


# POST /device
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.DeviceBase)
def create(request: schemas.DeviceBase,db: Session= Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support"))):
    return device.create(request,db)
    

# GET /device/{id}
@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowDevice)
def get_device(id:int, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    DeviceOutput = device.getDevice(id,db)
    if get_current_user.roles == "Admin":
        return DeviceOutput
    else:
        user = db.query(models.User).filter(models.User.email == get_current_user.email).first()
        if user.reseller_id == DeviceOutput.reseller_id:
            return DeviceOutput
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    

# PUT /device/{id}
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id:int,request: schemas.DeviceBase, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support"))):
    return device.updateDevice(id,request,db)


# DELETE /device/{id}
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support"))):
    return device.deleteDevice(id,db)
    
@router.get("/{id}/status",status_code=status.HTTP_200_OK,response_model=schemas.DeviceStatus)
def checkDevicestatus(id:int, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    return device.deviceStatus(id,db)

@router.get("/{id}/services",status_code=status.HTTP_200_OK,response_model=List[schemas.DeviceService])
def getServicesByDevice(id: int, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    DeviceOutput = device.getDevice(id,db)
    UserInfo = db.query(models.User).filter(models.User.email == get_current_user.email).first()
    if get_current_user.roles == "Admin" or get_current_user.roles == "Support":
        return service.getServicesByDevice(id,db)
    if DeviceOutput.reseller_id == UserInfo.reseller_id:
        return service.getServicesByDevice(id,db)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.get("/{id}/onu/autofind", status_code=status.HTTP_200_OK,response_model=List[schemas.Autofind])
def findONU(id:int,db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    DeviceOutput = device.getDevice(id,db)
    UserInfo = db.query(models.User).filter(models.User.email == get_current_user.email).first()
    if get_current_user.roles == "Admin" or get_current_user.roles == "Support":
        return device.findONU(id, db)
    if DeviceOutput.reseller_id == UserInfo.reseller_id:
        return device.findONU(id, db)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.post('/{id}/onu/search/sn',status_code=status.HTTP_200_OK,response_model=schemas.ONUSearchSNOutput)
def search(id,request:schemas.ONUSearchSN,db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    DeviceOutput = device.getDevice(id,db)
    UserInfo = db.query(models.User).filter(models.User.email == get_current_user.email).first()
    if get_current_user.roles == "Admin" or get_current_user.roles == "Support":
        return device.SearchONU(id,request,db)
    if DeviceOutput.reseller_id == UserInfo.reseller_id:
        return device.SearchONU(id,request,db)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.post('/{id}/onu/search/desc',status_code=status.HTTP_200_OK,response_model=List[schemas.SerachByDescriptionOuts])
def searchByDescription(id,request:schemas.SearchByDescription,db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    DeviceOutput = device.getDevice(id,db)
    UserInfo = db.query(models.User).filter(models.User.email == get_current_user.email).first()
    if get_current_user.roles == "Admin" or get_current_user.roles == "Support":
        return device.SearchONUByDesc(id,request,db)
    if DeviceOutput.reseller_id == UserInfo.reseller_id:
        return device.SearchONUByDesc(id,request,db)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.post('/{id}/onu/optical',status_code=status.HTTP_200_OK,response_model=schemas.OpticalPowerResponse)
def checkOpticalPower(id,request:schemas.OpticalPowerRequest,db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    data = {
        "FSP": request.FSP,
        "ONTID": request.ONTID,
    }
    UserInfo = db.query(models.User).filter(models.User.email == get_current_user.email).first()
    DeviceOutput = device.getDevice(id,db)
    if get_current_user.roles == "Admin" or get_current_user.roles == "Support":
        return device.CheckONUOptical(id,data,db)
    if DeviceOutput.reseller_id == UserInfo.reseller_id:
        return device.CheckONUOptical(id,data,db)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.delete("/{id}/onu/delete",status_code=status.HTTP_200_OK)
def deleteONU(id,request:schemas.ONUSearchSN,db:Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    UserInfo = db.query(models.User).filter(models.User.email == get_current_user.email).first()
    DeviceOutput = device.getDevice(id,db)
    if get_current_user.roles == "Admin" or get_current_user.roles == "Support":
        return device.deleteONU(id,request,db)
    if DeviceOutput.reseller_id == UserInfo.reseller_id:
        return device.deleteONU(id,request,db)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.post("/{id}/onu/add",status_code=status.HTTP_201_CREATED)
def addONU(id,request:schemas.AddONU,db:Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    DeviceOutput = device.getDevice(id,db)
    UserInfo = db.query(models.User).filter(models.User.email == get_current_user.email).first()
    if get_current_user.roles == "Admin" or get_current_user.roles == "Support":
        AddONUOutput =  device.addONU(id,request,db)
        data = AddONUOutput['data']
        if AddONUOutput["status"] == "failed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        data["AddedBy"] = get_current_user.email
        onudetails.create(data,db)
        print(data)
        return "Added"
    if DeviceOutput.reseller_id == UserInfo.reseller_id:
        AddONUOutput =  device.addONU(id,request,db)
        data = AddONUOutput['data']
        if AddONUOutput["status"] == "failed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        data["AddedBy"] = get_current_user.email
        onudetails.create(data,db)
        print(data)
        return "Added"
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.post('/{id}/onu/reset',status_code=status.HTTP_200_OK)
def checkOpticalPower(id,request:schemas.OpticalPowerRequest,db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support","Technicians"))):
    data = {
        "FSP": request.FSP,
        "ONTID": request.ONTID,
    }
    UserInfo = db.query(models.User).filter(models.User.email == get_current_user.email).first()
    DeviceOutput = device.getDevice(id,db)
    if get_current_user.roles == "Admin" or get_current_user.roles == "Support":
        return device.resetONU(id,data,db)
    if DeviceOutput.reseller_id == UserInfo.reseller_id:
        return device.resetONU(id,data,db)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)