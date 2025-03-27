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
