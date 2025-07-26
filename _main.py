from fastapi import FastAPI
from routes import identify_language
import os


app = FastAPI(
    debug=os.getenv("DEBUG", "false").lower() == "true", 
    title="Language Identifier model API", 
    description="API for managing language identification", 
    version="1.0.0"
)

# Include the identify_language router
app.include_router(
    identify_language.router, 
    prefix="/api", tags=["Language Identification"]
)
