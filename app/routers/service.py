from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models,oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import service
from ..middlewares import checkAdmin, role_required

router = APIRouter(
    tags=["Services"],
    prefix = "/service"
)

# GET /service
@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowServiceProfile])
def get_services(db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support"))):
    return service.getAll(db)
    



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowServiceProfile)
def create(request: schemas.ServiceProfile, db: Session=Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support"))):
    return service.create(request,db)
    



# GET /service/{id}
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowServiceProfile)
def get_service(id: int, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support"))):
    return service.getService(id,db)
    

# PUT /service/{id}

@router.put("/{id}",status_code=status.HTTP_200_OK)
def update_service(id: int, request: schemas.ServiceProfile, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support"))):
    return service.updateService(id,request,db)
    

# DELETE /service/{id}

@router.delete("/{id}",status_code=status.HTTP_200_OK)
def delete_service(id: int, db: Session = Depends(get_db),get_current_user:schemas.Reseller = Depends(role_required("Admin","Support"))):
    return service.deleteService(id,db)
    