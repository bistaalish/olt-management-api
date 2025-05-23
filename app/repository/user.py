
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .. import models,schemas
from ..hashing import Hash



def getAll(db: Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users
    
def getUserByReseller(reseller_id: int,db: Session):
    users = db.query(models.User).filter(models.User.reseller_id == reseller_id)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found for reseller with id {reseller_id}")
    return users
def create(request: schemas.User,db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password),role_id=request.role_id,reseller_id=request.reseller_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def resetPassword(user_id:int, request: schemas.ResetPassword,db: Session):
    if request.password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    user.password = Hash.bcrypt(request.password)
    db.commit()
    db.refresh(user)
    return user

def changePassword(User, request:schemas.ChangePassword, db:Session):
    print(User.password)
    if not Hash.verify(User.password,request.current_password):
        raise HTTPException(status_code=401, detail="Invalid current password")
    User.password = Hash.bcrypt(request.new_password)
    db.commit()
    db.refresh(User)
    return User

def getUser(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user

def deleteUser(user_id: int, db: Session):
    if user_id == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete the Admin user") 
    user = db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    db.commit()
    return "deleted"

def updateUser(user_id: int, request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    user.name = request.name
    user.email = request.email
    user.reseller_id = request.reseller_id
    # user.password = Hash.bcrypt(request.password)
    user.role_id = request.role_id
    db.commit()
    db.refresh(user)
    return "updated"

