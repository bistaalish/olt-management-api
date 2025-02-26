from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..repository import user


router = APIRouter(
    tags=["Users"],
    prefix = "/user"
)

'''
/user routes
'''

# POST /user
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser,tags=["Users"])
def create_user(request: schemas.User,db: Session= Depends(get_db)):
    # Create a new User
    return user.create(request,db)

# GET /user
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser],tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    return user.getAll(db)


# GET /user/{user_id}
@router.get("/{user_id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowUser,tags=["Users"])
def get_user(user_id: int, response: Response , db: Session = Depends(get_db)):
    return user.getUser(user_id,db)


# DELETE /user/{user_id}
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user.deleteUser(user_id,db)

# PUT /user/{user_id}
@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED,tags=["Users"])
def update_user(user_id: int, request: schemas.UserBase, db: Session = Depends(get_db)):
    return user.updateUser(user_id,request,db)
    # user = db.query(models.User).filter(models.User.id == user_id).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    # user.name = request.name
    # user.email = request.email
    # user.password = Hash.bcrypt(request.password)
    # user.reseller_id = request.reseller_id
    # db.commit()
    # db.refresh(user)
    # return "updated"