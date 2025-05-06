from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Reseller(Base):
    __tablename__ = "resellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    phone = Column(String(255))
    Location = Column(String(255))
    Descriptions = Column(String(255))
    users = relationship("User", back_populates="reseller")
    devices = relationship("Device", back_populates="reseller")

class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    roles = relationship("User", back_populates="roles")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    role_id = Column(Integer, ForeignKey('roles.id'))
    reseller_id = Column(Integer, ForeignKey('resellers.id'))
    reseller = relationship("Reseller", back_populates="users")
    roles = relationship("Roles", back_populates="roles")


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    vendor = Column(String(255))
    model = Column(String(255))
    type = Column(String(255))
    ip = Column(String(255), unique=True)
    Ctype = Column(String(255))
    username = Column(String(255))
    password = Column(String(255))
    SNMP_RO = Column(String(255))
    reseller_id = Column(Integer, ForeignKey('resellers.id'))
    reseller = relationship("Reseller", back_populates="devices")
    serviceprofiles = relationship("ServiceProfile", back_populates="device")
    discordWebhook = Column(String(255))
    
class ServiceProfile(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    serviceprofile_id = Column(String(255))
    lineprofile_id = Column(String(255))
    gemport = Column(String(255))
    vlan = Column(String(255))
    device_id = Column(Integer, ForeignKey('devices.id'))
    acs = Column(Boolean)
    acs_gemport = Column(String(255))
    acs_vlan = Column(String(255))
    device = relationship("Device", back_populates="serviceprofiles")

class ONUDetails(Base):
    __tablename__ = "onu_details"
    id = Column(Integer, primary_key=True, index=True)
    SN = Column(String(255))
    Description = Column(String(255))
    AddedBy = Column(String(255))
    Rx_OID = Column(String(255))
    Rx = Column(String(8))
    device_id = Column(Integer, ForeignKey('devices.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    reseller_id = Column(Integer, ForeignKey('resellers.id'))
