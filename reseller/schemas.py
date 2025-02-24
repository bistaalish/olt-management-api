from pydantic import BaseModel

class Reseller(BaseModel):
    name: str
    email: str
    phone: str

class ShowReseller(BaseModel):
    name: str
    email: str
    phone: str

    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str
    reseller_id: int