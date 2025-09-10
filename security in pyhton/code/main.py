from utils.exception import TokenBlocklistError
from fastapi import FastAPI,Depends
from utils.logs import configure_logger
from routes.route import  router
from security.tokens import  role_required

logger = configure_logger()
logger.info("Application started!")
app = FastAPI(title="User Manegment System")
app.include_router(router, prefix="/api", tags=["Auth"])


@app.get("/admin")
def admin_dashboard(user=Depends(role_required("admin"))):
    #return {"msg": "Welcome, Admin! You have full access."}
    return {
        "msg": "Welcome, Admin dash board.",
        "user": {
            "email": user.get("sub"),
            "role": user.get("role"),
                            }
    }
@app.get("/user")
def user_dashboard(user=Depends(role_required("user"))):
    return {
        "msg": "Welcome, user dash board.",
        "user": {
            "email": user.get("sub"),
            "role": user.get("role"),
                            }
    }
    #return {"msg": "Welcome, User! Limited access granted."}
