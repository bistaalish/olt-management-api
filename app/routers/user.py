from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models, oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..repository import user


router = APIRouter(
    tags=["Users"],
    prefix = "/user",
    
)

'''
/user routes
'''

# POST /user
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser,tags=["Users"])
def create_user(request: schemas.User,db: Session= Depends(get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    # Create a new User
    if get_current_user.reseller_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user.create(request,db)

# GET /user
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser],tags=["Users"])
def get_users(db: Session = Depends(get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    # Create a new User
    if get_current_user.reseller_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user.getAll(db)


# GET /user/{user_id}
@router.get("/{user_id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowUser,tags=["Users"])
def get_user(user_id: int, response: Response , db: Session = Depends(get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    # Create a new User
    User = user.getUser(user_id,db)
    if get_current_user.reseller_id != 1:
        if User.reseller_id == get_current_user.reseller_id:
            return User
        raise HTTPException(status_code=403, detail="Forbidden")
    return User


# DELETE /user/{user_id}
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    # Create a new User
    if get_current_user.reseller_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user.deleteUser(user_id,db)

# PUT /user/{user_id}
@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED,tags=["Users"])
def update_user(user_id: int, request: schemas.UserBase, db: Session = Depends(get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    # Create a new User
    if get_current_user.reseller_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user.updateUser(user_id,request,db)

