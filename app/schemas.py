from pydantic import BaseModel
from typing import List

class Reseller(BaseModel):
    name: str
    email: str
    phone: str

class User(BaseModel):
    name: str
    email: str
    password: str
    reseller_id: int

class ShowResellerUsers(BaseModel):
    name: str
    email: str

class ShowReseller(BaseModel):
    name: str
    email: str
    phone: str
    users: List[ShowResellerUsers] = []

    class Config():
        orm_mode = True



class ShowUser(BaseModel):
    name: str
    email: str
    reseller: Reseller
     
    class Config():
        orm_mode = True