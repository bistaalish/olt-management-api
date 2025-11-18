from pydantic import BaseModel, field_validator, ValidationError,Field
from typing import List, Optional

class AutofindData(BaseModel):
    FSP: str
    SN : str
#    vendorsn : str
#    vendorid : str

class Role(BaseModel):
    id: int
    name: str

class UserBase(BaseModel):
    name: str
    email: str
    role_id: int
    reseller_id: int

class User(UserBase):
    name: str
    email: str
    password: str
    role_id: int
    reseller_id: Optional[int]

class ResellerBase(BaseModel):
    name: str
    Descriptions: str

class Reseller(ResellerBase):
    name: str
    Descriptions: str
    users: List[User] = []

class ShowResellerUsers(BaseModel):
    id: int
    name: str


class ShowUserReseller(BaseModel):
    name: str
    id: int

    class Config():
        orm_mode = True

class ShowDeviceReseller(BaseModel):
    id: int
    name: str


class ShowReseller(BaseModel):
    id: int
    name: str
    Descriptions: str
    users: List[ShowResellerUsers]
    devices: List[ShowDeviceReseller]

    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    roles: Role
    reseller: Optional[ShowUserReseller]
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
    SNMP_RO: str
    discordWebhook: Optional[str]
    # class Config():
    #     orm_mode = True

class ShowDevice(BaseModel):
    id: int
    name: str
    ip: str



class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    roles: str

class DeviceBase(BaseModel):
    name: str
    ip: str
    username: str
    password: str
    reseller_id: int
    SNMP_RO: Optional[str] = None
    discordWebhook: Optional[str] = None
    class Config():
        orm_mode = True

class Device(BaseModel):
    name: str
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
    acs: Optional[bool]  = False
    acs_gemport: Optional[str] = None
    acs_vlan: Optional[str] = None
    acsprofile_id : Optional[str] = None

class ShowServiceProfile(BaseModel):
    id: int
    name: str
    serviceprofile_id: str
    lineprofile_id: str
    gemport: str
    vlan: str
    device: DeviceService
    acs: Optional[bool]  = False
    acs_gemport: Optional[str] = None
    acs_vlan: Optional[str] = None
    acsprofile_id : Optional[str] = None

class DeviceService(BaseModel):
    id : int
    vlan: str

class Autofind(BaseModel):
    Number: str
    FSP: str
    SN: str
    interface: str
    port: str
    VendorID: str
    Model: str
    

class ONUSearchSN(BaseModel):
    sn: str


class DeleteONU(BaseModel):
    FSP: str
    ONTID: str
    SN: str
    Description: str
    

class ONUSearchSNOutput(BaseModel):
    status: str
    Description: str
    FSP: str
    SN: str
    ONTID: str
    VendorSN: str
    Lastdowncause: str
    LineProfile: str

class AddONU(BaseModel):
    SN : str
    FSP: str
    interface: str
    port: str
    service_id: int
    description: str
    nativevlan:  Optional[bool]  = False

class ResetPassword(BaseModel):
    password: str
    confirm_password: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str

class SearchByDescription(BaseModel):
    description: str

class SerachByDescriptionOuts(BaseModel):
    Description: str
    SN: str
    FSP: str
    ONTID: str
    P: str
    Interface: str
    state: str

class DashBoardService(BaseModel):
    id: int
    name: str
    serviceprofile_id: str
    lineprofile_id: str
    gemport: str
    vlan: str

class DashboardDevice(BaseModel):
    id: int
    ip: str
    name: str
    serviceprofiles: List[DashBoardService]

class ONUOutput(BaseModel):
    id: int
    SN: str
    Description: str
    AddedBy: str

class DashboardOutput(BaseModel):
    deviceCount: int
    resellerCount: int
    ONUCount: int
    userCount: int


class OpticalPowerRequest(BaseModel):
    FSP: str
    ONTID: str
    
class OpticalPowerResponse(BaseModel):
    status: str
    ONU_RX: float


class DeviceStatus(BaseModel):
    status: str


class ONUModify(BaseModel):
    FSP: str
    ONTID: str
    Description: Optional[str] = None
    SN: Optional[str] = None
    service_id: Optional[int] = None

class ONTBase(BaseModel):
    FSP: str = Field(..., example="0/1/0")
    ONTID: int = Field(..., example=0)
    SN: str = Field(..., example="48575443A31B8151")
    desc: str = Field(..., example="schooldada-cctv")
    device_id: int = Field(default=2, example=2)