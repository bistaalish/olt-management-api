#!/bin/bash

# Activate venv
cd /home/alish/olt-management-api/ || exit 1
source .venv/bin/activate

# Launch the FastAPI app with uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --reload >> applog.txt 2>&1
