from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, user, stream
from app.database import connect_to_mongo

app = FastAPI(title="Vibie Backend")

# Allow CORS for frontend and Telegram Web App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Vibie backend!"}

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(stream.router, prefix="/stream", tags=["stream"])