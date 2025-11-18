from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas

# ----------------------
# CREATE
# ----------------------
def create_ont(db: Session, ont: schemas.ONTBase):
    db_ont = models.ONT(
        FSP=ont.FSP,
        ONTID=ont.ONTID,
        SN=ont.SN,
        desc=ont.desc,
        device_id=ont.device_id
    )
    db.add(db_ont)
    try:
        db.commit()
        db.refresh(db_ont)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create ONT: {str(e)}"
        )
    return db_ont

# ----------------------
# READ ALL
# ----------------------
def get_all_onts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ONT).offset(skip).limit(limit).all()

# ----------------------
# READ ONE
# ----------------------
def get_ont_by_id(db: Session, ont_id: int):
    ont = db.query(models.ONT).filter(models.ONT.id == ont_id).first()
    if not ont:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ONT with ID {ont_id} not found"
        )
    return ont

# ----------------------
# UPDATE
# ----------------------
def update_ont(db: Session, ont_id: int, ont_data: schemas.ONTBase):
    ont = db.query(models.ONT).filter(models.ONT.id == ont_id).first()
    if not ont:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ONT with ID {ont_id} not found"
        )
    ont.FSP = ont_data.FSP
    ont.ONTID = ont_data.ONTID
    ont.SN = ont_data.SN
    ont.desc = ont_data.desc
    ont.device_id = ont_data.device_id
    db.commit()
    db.refresh(ont)
    return ont

# ----------------------
# DELETE
# ----------------------
def delete_ont(db: Session, ont_id: int):
    ont = db.query(models.ONT).filter(models.ONT.id == ont_id).first()
    if not ont:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ONT with ID {ont_id} not found"
        )
    db.delete(ont)
    db.commit()
    return {"detail": f"ONT with ID {ont_id} deleted"}
