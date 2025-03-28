from fastapi import FastAPI, Depends, status, Response, HTTPException, Request
from . import schemas, models, hashing
# from typing import List
from .database import engine,get_db,SessionLocal,check_and_create_reseller
from fastapi.middleware.cors import CORSMiddleware
from .repository import reseller as RepositoryReseller

# from sqlalchemy.orm import Session
# from .hashing import Hash
from .routers import reseller,user,auth,device,service,onu
import uvicorn
import time
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define allowed origins

app = FastAPI()
# Configure Logging
logging.basicConfig(
    filename="http_logs.log",  # Save logs to a file
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Allow all origins (accessible from any IP)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Read request body (need to store as body can be read only once)
    body = await request.body()
    
    # Log request details
    logging.info(f"Request: {request.method} {request.url}")
    logging.info(f"Headers: {dict(request.headers)}")
    logging.info(f"Body: {body.decode('utf-8') if body else None}")

    # Process request and get response
    response = await call_next(request)
    
    # Get response body
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    response = Response(response_body, status_code=response.status_code, headers=dict(response.headers))

    # Log response details
    duration = time.time() - start_time
    logging.info(f"Response: {response.status_code} | Duration: {duration:.4f}s")
    logging.info(f"Response Body: {response_body.decode('utf-8') if response_body else None}\n")

    return response
models.Base.metadata.create_all(engine)

@app.on_event("startup")
def startup():
    db = SessionLocal()
    check_and_create_reseller(db)
    db.close()
# Include the auth router
app.include_router(auth.router)
# Include the reseller router
app.include_router(reseller.router)

#Include the user router
app.include_router(user.router)

# Include the device router
app.include_router(device.router)

# Include the service router
app.include_router(service.router)

# Include the ONU details
app.include_router(onu.router)