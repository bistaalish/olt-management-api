from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from typing import List
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
/reseller routes
'''
@app.post("/reseller",status_code=status.HTTP_201_CREATED)
def create(request: schemas.Reseller,db: Session= Depends(get_db)):
    # Create a new Reseller
    reseller = db.query(models.Reseller).filter(models.Reseller.name == request.name).first()
    if reseller:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reseller with this name already exists")
    newReseller = models.Reseller(name=request.name,email=request.email,phone=request.phone)
    db.add(newReseller)
    db.commit()
    db.refresh(newReseller)
    return newReseller

# GET /reseller
@app.get("/reseller", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowReseller])
def get_resellers(db: Session = Depends(get_db)):
    resellers = db.query(models.Reseller).all()
    if not resellers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resellers found")
    return resellers

# GET /reseller/{reseller_id}
@app.get("/reseller/{reseller_id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowReseller)
def get_reseller(reseller_id: int, response: Response , db: Session = Depends(get_db)):
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not reseller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reseller with id {reseller_id} not found")
    return reseller

# DELETE /reseller/{reseller_id}
@app.delete("/reseller/{reseller_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reseller(reseller_id: int, db: Session = Depends(get_db)):
    if reseller_id == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete the Admin reseller")
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).delete(synchronize_session=False)
    if not reseller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reseller with id {reseller_id} not found")
    db.commit()
    return "deleted"  



# PUT /reseller/{reseller_id}
@app.put("/reseller/{reseller_id}", status_code=status.HTTP_202_ACCEPTED)
def update_reseller(reseller_id: int, request: schemas.Reseller, db: Session = Depends(get_db)):
    if reseller_id == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update the Admin reseller")
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not reseller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reseller with id {reseller_id} not found")
    reseller.name = request.name
    reseller.email = request.email
    reseller.phone = request.phone
    db.commit()
    db.refresh(reseller)
    return "updated"



'''User Routes'''
@app.post("/user",status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User,db: Session= Depends(get_db)):
    # Create a new User
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    new_user = models.User(name=request.name,email=request.email,password=request.password,reseller_id=request.reseller_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user