from pydantic import BaseModel, Field, field_validator, model_validator


class Description(BaseModel):
    type: str
    value: str
    color: str | None = None
    name: str


class Action(BaseModel):
    type: str
    name: str
    link: str


class Tag(BaseModel):
    internal_name: str
    name: str
    category: str
    category_name: str
    color: str | None = None


class AssetClassInfoItem(BaseModel):
    classid: int
    icon_url: str
    icon_url_large: str
    icon_drag_url: str
    name: str
    market_hash_name: str
    market_name: str
    name_color: str
    background_color: str
    type: str
    tradable: str
    marketable: str
    commodity: str
    market_tradable_restriction: str
    market_marketable_restriction: str
    descriptions: list[Description] = Field(default_factory=list)
    owner_descriptions: str
    actions: list[Action] = Field(default_factory=list)
    market_actions: list[Action] = Field(default_factory=list)
    tags: list[Tag] = Field(default_factory=list)

    @field_validator("descriptions", "actions", "market_actions", "tags", mode="before")
    def _ensure_list(cls, v):
        if v is None:
            return []
        if isinstance(v, dict):
            return list(v.values())
        return v


class AssetClassInfo(BaseModel):
    result: dict[int, AssetClassInfoItem] | None = None
    error: str | None = None
    success: bool

    @model_validator(mode="before")
    def _extract_success_from_result(cls, data):
        res = data.get("result")
        if isinstance(res, dict) and "success" in res:
            data["success"] = res.pop("success")
        return data
