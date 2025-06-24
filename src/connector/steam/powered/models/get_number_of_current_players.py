from pydantic import BaseModel


class NumberOfCurrentPlayersResponse(BaseModel):
    player_count: int
    result: int


class NumberOfCurrentPlayers(BaseModel):
    response: NumberOfCurrentPlayersResponse
