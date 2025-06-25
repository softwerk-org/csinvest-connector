from pydantic import BaseModel


class Friend(BaseModel):
    steamid: str
    relationship: str
    friend_since: int


class FriendsList(BaseModel):
    friends: list[Friend]


class FriendList(BaseModel):
    friendslist: FriendsList
