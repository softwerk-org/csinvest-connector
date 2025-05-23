from pydantic import BaseModel


class Description(BaseModel):
    type: str
    value: str
    color: str
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
    color: str


class AssetClassInfoItem(BaseModel):
    classid: str
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
    descriptions: list[Description]
    owner_descriptions: str
    actions: list[Action]
    market_actions: list[Action]
    tags: list[Tag]


class AssetClassInfoError(BaseModel):
    error: str
    success: bool


class AssetClassInfo(BaseModel):
    result: dict[str, AssetClassInfoItem] | AssetClassInfoError
