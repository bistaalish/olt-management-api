from fastapi import APIRouter, Depends, status, Response, HTTPException
from . import schemas, oauth2

def role_required(*required_roles: str):
    def wrapper(current_user: dict = Depends(oauth2.get_current_user)):
        if current_user.roles not in required_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return wrapper

# # Universal admin check
def checkAdmin(get_current_user: schemas.Reseller = Depends(oauth2.get_current_user)):
    """Dependency to check if the user is an Admin (role_id == 1)."""
    if get_current_user.role_id == 1:
        return get_current_user    
    raise HTTPException(status_code=403, detail="Forbidden")
    
# # Check if user is Support Only.
# def checkSupport(get_current_user: schemas.Reseller = Depends(oauth2.get_current_user)):
#     if get_current_user.role_id == 2:
#         return get_current_user    
#     raise HTTPException(status_code=403, detail="Forbidden")

# #Check if user if FiledStaff
# def checkFieldStaff(get_current_user: schemas.Reseller = Depends(oauth2.get_current_user)):
#     if get_current_user.role_id == 3:
#         return get_current_user    
#     raise HTTPException(status_code=403, detail="Forbidden")
# # Check if the user is an Administrator or Support
# def checkAdminOrSupport(get_current_user: schemas.Reseller = Depends(oauth2.get_current_user)):
#     if get_current_user.role_id == 1 or get_current_user.role_id == 2:
#         return get_current_user
#     raise HTTPException(status_code=403, detail="Forbidden")
     
# # Check if the user is an Administrator or Support or FieldStaff
# def checkAdminOrSupportorFieldStaff(get_current_user: schemas.Reseller = Depends(oauth2.get_current_user)):
#     if get_current_user.role_id == 1 or get_current_user.role_id == 2 or get_current_user.role_id == 3:
#         return get_current_user
#     raise HTTPException(status_code=403, detail="Forbidden")