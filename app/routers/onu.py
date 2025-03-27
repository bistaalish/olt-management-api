from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models,oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import device,service,onudetails

router = APIRouter(
    tags=["ONU"],
    prefix = "/onu"
)
