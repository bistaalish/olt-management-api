from pydantic import BaseModel, field_validator, ValidationError,Field
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

class Device(BaseModel):
    name: str
    vendor: str
    model: str
    type: str
    ip: str
    username: str
    password: str
    reseller: ShowUserReseller

    class Config():
        orm_mode = True

class DeviceService(BaseModel):
    id: int
    name: str


class ServiceProfile(BaseModel):
    name: str
    serviceprofile_id: str
    lineprofile_id: str
    gemport: str
    vlan: str
    device_id: int

class ShowServiceProfile(BaseModel):
    id: int
    name: str
    serviceprofile_id: str
    lineprofile_id: str
    gemport: str
    vlan: str
    device: DeviceService

class Autofind(BaseModel):
    SN: str
    FSP: str
    interface: str
    port: str

class ONUSearchSN(BaseModel):
    sn: str = Field(..., min_length=16, max_length=16)


class ONUSearchSNOutput(BaseModel):
    FSP: str
    ONTID: str
    sn: str
    VendorSN: str
    Description: str
    LineProfile: str