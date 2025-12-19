from fastapi import Depends, HTTPException, Query, UploadFile, File
from fastapi.routing import APIRouter
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
import logging
from app.core.crypto import hash_password, verify_hash
from app.schema.user import UserCreate, UserResponse, UserLogin
from app.schema.token import TokenResponse

from app.models.rides import Users
from app.db.session import get_session
from app.auth.oauth2 import get_current_user, create_access_token

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    # Check if username or email already exists
    result = await session.exec(
        select(Users).where(
            (Users.username == user_data.username) | (
                Users.email == user_data.email)
        )
    )
    existing_user = result.first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )

    # Create new user
    hashed_password = hash_password(user_data.password)
    db_user = Users(
        username=user_data.username,
        password_hash=hashed_password,
        name=user_data.name,
        email=user_data.email,
        phone_number=user_data.phone_number
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    # Auto-login: create access token for the new user
    from datetime import timedelta
    access_token_expires = timedelta(minutes=300)
    access_token = create_access_token(
        data={"sub": db_user.username, "pwd_hash": db_user.password_hash},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(**db_user.dict())
    )


@router.post("/login")
async def login_user(login_data: UserLogin, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Users).where(Users.username == login_data.username))
    user = result.first()

    if not user or not verify_hash(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    
    access_token = create_access_token(
        data={"sub": user.username, "pwd_hash": user.password_hash},
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: Users = Depends(get_current_user)):
    return UserResponse(**current_user.dict())


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(session: AsyncSession = Depends(get_session), current_user: Users = Depends(get_current_user)):
    result = await session.exec(select(Users))
    users = result.all()
    return [UserResponse(**user.dict()) for user in users]
