from fastapi import APIRouter, Depends, status, Response, HTTPException
from . import schemas, oauth2

# Universal admin check
def checkAdmin(get_current_user: schemas.Reseller = Depends(oauth2.get_current_user)):
    """Dependency to check if the user is an Admin (role_id == 1)."""
    if get_current_user.role_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return get_current_user