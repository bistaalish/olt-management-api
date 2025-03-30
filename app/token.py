from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from . import schemas
import os
from dotenv import load_dotenv
from .database import SessionLocal, get_db
from . import models

# Load environment variables from .env file
load_dotenv()

# Replace with your own secret key
SECRET_KEY = str(os.getenv('SECRET_KEY'))
ALGORITHM = str(os.getenv('ALGORITHM'))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        email: str = payload.get("sub")
        role_id: str = payload.get("role_id")
        # print(email, role_id)
        if email is None:
            raise credentials_exception
        if role_id is None:
            raise credentials_exception
        return schemas.TokenData(email=email,role_id=role_id)
    except JWTError:
        raise credentials_exception 