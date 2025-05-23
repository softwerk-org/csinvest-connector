from pydantic import BaseModel


class PlayerSummariesResponsePlayer(BaseModel):
    steamid: str | None
    communityvisibilitystate: int | None
    profilestate: int | None
    personaname: str | None
    profileurl: str | None
    avatar: str | None
    avatarmedium: str | None
    avatarfull: str | None
    avatarhash: str | None
    personastate: int | None
    primaryclanid: str | None
    timecreated: int | None
    personastateflags: int | None
    loccountrycode: str | None
    locstatecode: str | None


class PlayerSummariesResponse(BaseModel):
    players: list[PlayerSummariesResponsePlayer]


class PlayerSummaries(BaseModel):
    response: PlayerSummariesResponse
