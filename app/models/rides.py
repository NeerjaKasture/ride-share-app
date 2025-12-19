from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class RideUserLink(SQLModel, table=True):
    ride_id: Optional[int] = Field(default=None, foreign_key="rides.ride_id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    name: str
    role: str = Field(default="user")
    email: str = Field(index=True, unique=True)
    phone_number: str

    # rides they created
    created_rides: List["Rides"] = Relationship(back_populates="creator")

    # rides they joined (as participant)
    rides: List["Rides"] = Relationship(back_populates="participants", link_model=RideUserLink)

class Rides(SQLModel, table=True):
    ride_id: Optional[int] = Field(default=None, primary_key=True)
    creator_id: int = Field(foreign_key="users.id")   # owner of the ride
    start_location: str
    end_location: str
    scheduled_at: datetime
    created_at: datetime = Field(default_factory=datetime.now)

    # relationship back to creator
    creator: Users = Relationship(back_populates="created_rides")

    # other participants
    participants: List[Users] = Relationship(back_populates="rides", link_model=RideUserLink)
