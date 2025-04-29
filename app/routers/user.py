from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models, oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..repository import user
from ..middlewares import checkAdmin, role_required


router = APIRouter(
    tags=["Users"],
    prefix = "/user",
    
)

'''
/user routes
'''

# POST /user
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
def create_user(request: schemas.User,db: Session= Depends(get_db),get_current_user:schemas.User= Depends(role_required("Admin"))):
    return user.create(request,db)


@router.post("/{user_id}/reset-password", status_code=status.HTTP_200_OK)
def reset_password(user_id: int,request: schemas.ResetPassword,db: Session= Depends(get_db),get_current_user:schemas.User= Depends(role_required("Admin"))):
    print(get_current_user.roles)
    if get_current_user.roles == "Admin":
        user.resetPassword(user_id, request, db)
        return {"message": "Password reset successful"}
    raise HTTPException(status_code=403, detail="Forbidden")

@router.post("/{user_id}/change_password",status_code=status.HTTP_200_OK)
def change_password(user_id: int,request: schemas.ChangePassword,db: Session= Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    User = user.getUser(user_id,db)
    if get_current_user.email != User.email:
        raise HTTPException(status_code=403, detail="Forbidden")
    user.changePassword(User, request, db)
    return {"message": "Password changed successful"}

# GET /user
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(get_db),get_current_user:schemas.User= Depends(role_required("Admin"))):
    return user.getAll(db)


# GET /user/{user_id}
@router.get("/{user_id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowUser)
def get_user(user_id: int, response: Response , db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    # Create a new User
    User = user.getUser(user_id,db)
    if get_current_user.roles == "Admin" or User.email == get_current_user.email:
            return User
    raise HTTPException(status_code=403, detail="Forbidden")
    

# DELETE /user/{user_id}
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db),get_current_user:schemas.User= Depends(role_required("Admin"))):
    # Create a new User
    if get_current_user.roles != "Admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return user.deleteUser(user_id,db)

# PUT /user/{user_id}
@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, request: schemas.UserBase, db: Session = Depends(get_db),get_current_user:schemas.User= Depends(role_required("Admin"))):
    # Create a new User
    User = user.getUser(user_id,db)
    if get_current_user.roles == "Admin" or User.email == get_current_user.email:
        return user.updateUser(user_id,request,db)
    raise HTTPException(status_code=403, detail="Forbidden")

