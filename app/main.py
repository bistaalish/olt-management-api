from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, hashing
from typing import List
from .database import engine,get_db,SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash
from .routers import reseller,user
app = FastAPI()

models.Base.metadata.create_all(engine)

# Include the reseller router
app.include_router(reseller.router)

#Include the user router
app.include_router(user.router)

'''User Routes'''

