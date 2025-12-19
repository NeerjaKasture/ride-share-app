from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Forward reference for UserPicture
class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    email: str
    phone_number: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    role: str
    email: str
    phone_number: str

class RideCreate(BaseModel):
    start_location: str
    end_location: str
    scheduled_at: datetime

class RideResponse(BaseModel):
    ride_id: int
    creator_id: int
    start_location: str
    end_location: str
    scheduled_at: datetime
    created_at: datetime
    creator: UserResponse
    participants: List[UserResponse]
