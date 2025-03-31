from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from . import models
from .hashing import Hash
# Load environment variables
load_dotenv()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./flink.db"
# MySQL Database URL
MYSQL_USER = str(os.getenv("MYSQL_USER"))
MYSQL_PASSWORD = str(os.getenv("MYSQL_PASSWORD"))
MYSQL_HOST = str(os.getenv("MYSQL_HOST", "localhost"))
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DATABASE = str(os.getenv("MYSQL_DATABASE"))

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# Check if Admin Role exists in database
def checkAdminRole(db: Session):
    adminRole = db.query(models.Roles).filter(models.Roles.name == "Admin").first()
    if not adminRole:
        return False
    return True

# Create admin Role
def createAdminRole(db: Session):
    adminRole = models.Roles(id=1,name="Admin")
    db.add(adminRole)
    db.commit()
    db.refresh(adminRole)
    print(f"Created Admin role with id={adminRole.id}")

# Check if Admin User exists in database
def checkAdminUser(db: Session):
    adminUser =  db.query(models.User).filter(models.User.name == "Admin").first()
    if not adminUser:
        return False
    return True

# Create Admin User
def createAdminUser(db: Session):
    adminUser =  models.User(id=1, name="Admin", email="admin@example.com", password=Hash.bcrypt("admin123!"),role_id=1)
    db.add(adminUser)
    db.commit()
    db.refresh(adminUser)
    print(f"Created Admin User with id={adminUser.id}")

# Create Admin Role and User if not exists
def CreateAdminRoleAndUserIfNotExists(db: Session):
    if not checkAdminRole(db):
        createAdminRole(db)
    if not checkAdminUser(db):
        createAdminUser(db)