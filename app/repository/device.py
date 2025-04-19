from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .. import models,schemas
from ..hashing import Hash
from ..utils import Huawei
from ..repository import onudetails
def getAll(db:Session):
    devices = db.query(models.Device).all()
    if not devices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No devices found")
    return devices

def getDeviceByResellerId(db:Session,id:int):
    if id == 1:
        devices = db.query(models.Device).all()
    else:
        devices = db.query(models.Device).filter(models.Device.reseller_id == id).all()
    if not devices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No devices found")
    return devices


def create(request: schemas.Device, db: Session):
    device = db.query(models.Device).filter(models.Device.ip == request.ip).first()
    if device:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Device with this IP already exists")
    newDevice = models.Device(name=request.name,vendor=request.vendor,model=request.model,type=request.type,ip=request.ip,username=request.username,password=request.password,SNMP_RO=request.SNMP_RO,reseller_id=request.reseller_id)
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
        print(autofindResults["status"])
        if autofindResults["status"] == "failed":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ONU Found on Autofind")
    return autofindResults['devices']

def SearchONU(id,request:schemas.ONUSearchSN,db: Session):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    tn = Huawei.TelnetSession(device)
    SearchOutput = Huawei.SearchBySN(request.sn,tn)
    if (SearchOutput['status'] == "failed"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{request.sn} not Found in Provided OLT")
    return SearchOutput["device"]
    
def SearchONUByDesc(id:int,request,db:Session):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    tn = Huawei.TelnetSession(device)
    SearchOutput = Huawei.searchByDesc(request.description,tn)
    print(SearchONUByDesc)
    if (SearchOutput['status'] == "failed"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{request.description} not Found in Provided OLT")
    return SearchOutput["device"]

def deleteONU(id,request:schemas.ONUSearchSN,db:Session):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    tn = Huawei.TelnetSession(device)
    SearchOutput = Huawei.SearchBySN(request.sn,tn)
    if (SearchOutput['status'] == "failed"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{request.sn} not Found in Provided OLT")
    DeleteOutput = Huawei.deleteONU(tn,SearchOutput['device'])
    print(DeleteOutput['status'])
    if DeleteOutput['status'] == 'failed':
        print(DeleteOutput['error'])
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail=DeleteOutput['error'])
    # print(DeleteOutput)
    # onudetails.deleteONUEntry(request.sn,db)
    return "deleted"

def addONU(id,request: schemas.AddONU,db:Session):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    service = db.query(models.ServiceProfile).filter(models.ServiceProfile.id == request.service_id).first()
    data = {
        "sn" : request.SN,
        "FSP" : request.FSP,
        "interface" : request.interface,
        "port" : request.port,
        "vlan" : service.vlan,
        "description" : request.description,
        "gemport"  : service.gemport,
        "serviceProfileId" : service.serviceprofile_id,
        "lineProfileId" : service.lineprofile_id,
        "acs" : service.acs,
        "acs_gemport" : service.acs_gemport,
        "acs_vlan" : service.acs_vlan,
        "nativevlan" : request.nativevlan
    }
    tn = Huawei.TelnetSession(device)
    AddOuput = Huawei.AddONU(tn,data)
    if AddOuput['status'] == 'failed':
        print(AddOuput['error'])
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail=AddOuput['error'])
    OutputData = AddOuput['data']
    OutputData["device_id"] = device.id
    OutputData["service_id"] = service.id
    OutputData['reseller_id'] = device.reseller_id
    AddOuput["data"] = OutputData
    return AddOuput

def CheckONUOptical(id,data,db):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    tn = Huawei.TelnetSession(device)
    outputData = Huawei.getOpticalInfo(tn,data)
    return outputData