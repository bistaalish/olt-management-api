from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Reseller(Base):
    __tablename__ = "resellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    users = relationship("User", back_populates="reseller")
    devices = relationship("Device", back_populates="reseller")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    reseller_id = Column(Integer, ForeignKey('resellers.id'))
    reseller = relationship("Reseller", back_populates="users")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    vendor = Column(String)
    model = Column(String)
    type = Column(String)
    ip = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
    reseller_id = Column(Integer, ForeignKey('resellers.id'))
    reseller = relationship("Reseller", back_populates="devices")
    serviceprofiles = relationship("ServiceProfile", back_populates="device")
    
class ServiceProfile(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    serviceprofile_id = Column(String)
    lineprofile_id = Column(String)
    gemport = Column(String)
    vlan = Column(String)
    device_id = Column(Integer, ForeignKey('devices.id'))
    acs = Column(Boolean)
    acs_gemport = Column(String)
    acs_vlan = Column(String)
    device = relationship("Device", back_populates="serviceprofiles")

class ONUDetails(Base):
    __tablename__ = "onu_details"
    id = Column(Integer, primary_key=True, index=True)
    SN = Column(String)
    Description = Column(String)
    device_id = Column(Integer, ForeignKey('devices.id'))
    serviceprofile_id = Column(Integer, ForeignKey('services.id'))
