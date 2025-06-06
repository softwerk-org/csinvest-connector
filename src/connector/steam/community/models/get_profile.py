# generated by datamodel-codegen:
#   filename:  <stdin>
#   timestamp: 2025-05-09T20:58:30+00:00

from __future__ import annotations

from pydantic import BaseModel, Field


class ProfileProfile(BaseModel):
    steam_id64: str | None = Field(None, alias="steamID64")
    steam_id: str | None = Field(None, alias="steamID")
    online_state: str | None = Field(None, alias="onlineState")
    state_message: str | None = Field(None, alias="stateMessage")
    privacy_state: str | None = Field(None, alias="privacyState")
    visibility_state: str | None = Field(None, alias="visibilityState")
    avatar_icon: str | None = Field(None, alias="avatarIcon")
    avatar_medium: str | None = Field(None, alias="avatarMedium")
    avatar_full: str | None = Field(None, alias="avatarFull")
    vac_banned: str | None = Field(None, alias="vacBanned")
    trade_ban_state: str | None = Field(None, alias="tradeBanState")
    is_limited_account: str | None = Field(None, alias="isLimitedAccount")
    custom_url: None = Field(None, alias="customURL")
    member_since: str | None = Field(None, alias="memberSince")
    steam_rating: None = Field(None, alias="steamRating")
    hours_played2_wk: str | None = Field(None, alias="hoursPlayed2Wk")
    headline: None
    location: str | None
    realname: None
    summary: str | None


class Profile(BaseModel):
    profile: ProfileProfile
