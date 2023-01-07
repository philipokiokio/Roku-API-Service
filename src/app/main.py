from fastapi import FastAPI, status
from src.app.database import SQLALCHEMY_DB_URL







app = FastAPI()






@app.get("/", status_code= status.HTTP_200_OK )
def server_root():
    return {
        "message": "Hello, I am Roku the Server",
        "docs": "/docs"
    }