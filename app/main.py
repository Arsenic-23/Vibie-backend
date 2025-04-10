from fastapi import FastAPI

app = FastAPI(title="Vibie Backend")

@app.get("/")
def read_root():
    return {"message": "Welcome to Vibie backend!"}
from app.routes import auth, user, stream
from app.database import connect_to_mongo
from app.routes import websocket
app.include_router(websocket.router, tags=["websocket"])
app = FastAPI(title="Vibie Backend")

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# Register all route modules
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(stream.router, prefix="/stream", tags=["stream"])