from pydantic import BaseModel
from typing import List, Optional 

class UserBase(BaseModel):
    name: str
    email: str
    reseller_id: int

class User(UserBase):
    name: str
    email: str
    password: str
    reseller_id: int

class ResellerBase(BaseModel):
    name: str
    email: str
    phone: str

class Reseller(ResellerBase):
    name: str
    email: str
    phone: str
    users: List[User] = []

class ShowResellerUsers(BaseModel):
    name: str
    email: str

class ShowUserReseller(BaseModel):
    name: str
    id: int
    class Config():
        orm_mode = True
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
    reseller: ShowUserReseller
     
    class Config():
        orm_mode = True

class Device(BaseModel):
    name: str
    vendor: str
    model: str
    type: str
    ip: str
    username: str
    password: str

    class Config():
        orm_mode = True

class ShowDevice(BaseModel):
    name: str
    vendor: str
    model: str
    type: str
    ip: str
    username: str

class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class DeviceBase(BaseModel):
    name: str
    vendor: str
    model: str
    type: str
    ip: str
    username: str
    password: str
    reseller_id: int

    class Config():
        orm_mode = True

class Device(DeviceBase):
    name: str
    vendor: str
    model: str
    type: str
    ip: str
    username: str
    password: str
    reseller: List [ResellerBase] = []

    class Config():
        orm_mode = True