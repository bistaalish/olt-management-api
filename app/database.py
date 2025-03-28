from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

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