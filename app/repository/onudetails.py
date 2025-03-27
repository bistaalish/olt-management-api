from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .. import models,schemas
from ..hashing import Hash

def create(data, db: Session):
    db.query(models.ONUDetails).filter(models.ONUDetails.SN == data["SN"]).delete(synchronize_session=False)
    new_ONU = models.ONUDetails(SN=data["SN"],Description=data["Description"],AddedBy=data["AddedBy"],device_id=data["device_id"],service_id=data["service_id"])
    db.add(new_ONU)
    db.commit()
    db.refresh(new_ONU)
    return data

def deleteONUEntry(sn, db: Session):
    ONU = db.query(models.ONUDetails).filter(models.ONUDetails.SN == sn).delete(synchronize_session=False)
    if not ONU:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ONU with SN {sn} not found")
    db.commit()
    return "deleted"

def getAll(db: Session):
    ONUs = db.query(models.ONUDetails).all()
    if not ONUs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ONUs found")
    return ONUs

