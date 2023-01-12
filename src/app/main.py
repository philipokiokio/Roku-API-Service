from fastapi import FastAPI, status
from src.auth.auth_router import user_router
from src.workspace.workspace_router import workspace_router

app = FastAPI()

app.include_router(user_router)
app.include_router(workspace_router)


@app.get("/", status_code=status.HTTP_200_OK)
def server_root():
    return {"message": "Hello, I am Roku the Server", "docs": "/docs"}
