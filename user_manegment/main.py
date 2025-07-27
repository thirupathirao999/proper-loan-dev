from fastapi import FastAPI
from route import  router


app = FastAPI(title="User Manegment System")
app.include_router(router, prefix="/api/v1", tags=["Auth"])








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