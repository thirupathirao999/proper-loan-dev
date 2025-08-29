from exception import TokenBlocklistError
from fastapi import FastAPI,Depends
from logs import configure_logger
from route import  router
from tokens import get_current_user, is_token_blacklisted, role_required,oauth2

logger = configure_logger()
logger.info("Application started!")
app = FastAPI(title="User Manegment System")
app.include_router(router, prefix="/api", tags=["Auth"])


@app.get("/admin")
def admin_dashboard(user=Depends(role_required("admin"))):
    #return {"msg": "Welcome, Admin! You have full access."}
    return {
        "msg": "Welcome, Admin! You have full access.",
        "user": {
            "email": user.get("sub"),
            "role": user.get("role"),
                            }
    }

@app.get("/user")
def user_dashboard(user=Depends(role_required("user"))):
    return {
        "msg": "Welcome, Admin! You have full access.",
        "user": {
            "email": user.get("sub"),
            "role": user.get("role"),
                            }
    }
    #return {"msg": "Welcome, User! Limited access granted."}





# from app.core.logging import configure_logger

# # Configure logger
# logger = configure_logger()

# # Create a Fast API
# fastapp = FastAPI()

# # Include account related routes in accounts_router 
# # V1 Routes
# fastapp.include_router(router, prefix="/api/v1")

# # V2 Routes
# fastapp.include_router(router, prefix="/api/v2")