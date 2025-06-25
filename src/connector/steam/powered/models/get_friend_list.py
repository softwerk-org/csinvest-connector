from datetime import datetime
from pydantic import BaseModel


class Friend(BaseModel):
    steamid: str
    relationship: str
    friend_since: datetime


class FriendsList(BaseModel):
    friends: list[Friend]


class FriendList(BaseModel):
    friendslist: FriendsList
