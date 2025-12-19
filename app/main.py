from fastapi import FastAPI
from app.api.v1.user import router as user_router
from app.auth.oauth2 import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ride Share API",
              description="A ride sharing application API", version="1.0.0")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Ride Share API", "docs": "/docs", "redoc": "/redoc"}

app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
