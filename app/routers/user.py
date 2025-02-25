from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter()

'''
/user routes
'''

# POST /user
@router.post("/user",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser,tags=["Users"])
def create_user(request: schemas.User,db: Session= Depends(get_db)):
    # Create a new User
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password),reseller_id=request.reseller_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# GET /user
@router.get("/user", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser],tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users

# GET /user/{user_id}
@router.get("/user/{user_id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowUser,tags=["Users"])
def get_user(user_id: int, response: Response , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user

# DELETE /user/{user_id}
@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT,tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if user_id == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete the Admin user") 
    user = db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    db.commit()
    return "deleted"

# PUT /user/{user_id}
@router.put("/user/{user_id}", status_code=status.HTTP_202_ACCEPTED,tags=["Users"])
def update_user(user_id: int, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    user.name = request.name
    user.email = request.email
    user.password = Hash.bcrypt(request.password)
    user.reseller_id = request.reseller_id
    db.commit()
    db.refresh(user)
    return "updated"