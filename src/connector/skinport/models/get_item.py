from datetime import date
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, RootModel


class Tag(BaseModel):
    name: str
    name_localized: str


class GVColorTint(BaseModel):
    W: float
    X: float
    Y: float
    Z: float


class MaterialProperties(BaseModel):
    g_tColor: str
    g_tNormal: str
    g_tMetalness: str | None = None
    g_vColorTint: GVColorTint
    g_tAmbientOcclusion: str | None = None
    g_flPearlescentScale: float | None = None


class Material(BaseModel):
    name: str
    painted: bool
    material: MaterialProperties


class WebGLStatic(BaseModel):
    name: str
    itemtype: str
    meshname: str
    classname: str
    materials: List[Material]
    paintname: str
    paintseed: int
    paintwear: float
    offlineurl: str
    attachments: List[Any]
    legacymodel: bool


class WebGLTexture(BaseModel):
    path: str


class WebGLDynamic(RootModel[Dict[str, WebGLTexture]]):
    root: Dict[str, WebGLTexture]


class WebGL(BaseModel):
    static: WebGLStatic
    dynamic: WebGLDynamic


class PublicItem(BaseModel):
    id: int
    saleId: int
    shortId: str
    productId: int
    assetId: int
    itemId: int
    appid: int
    steamid: str
    url: str
    family: str
    family_localized: str
    name: str
    title: str
    text: str
    marketName: str
    marketHashName: str
    color: str
    bgColor: str | None = None
    image: str
    classid: str
    assetid: str
    lock: str | None = None
    version: str
    versionType: str
    stackAble: bool
    suggestedPrice: int
    salePrice: int
    currency: str
    saleStatus: str
    saleType: str
    category: str
    category_localized: str
    subCategory: str
    subCategory_localized: str
    pattern: int
    finish: int | None = None
    customName: str | None = None
    wear: float | None = None
    link: str
    type: str
    exterior: str | None = None
    quality: str
    rarity: str
    rarity_localized: str
    rarityColor: str
    collection: str | None = None
    collection_localized: str | None = None
    stickers: List[Any]
    charms: List[Any]
    canHaveScreenshots: bool
    screenshots: List[str]
    souvenir: bool
    stattrak: bool
    tags: List[Tag]
    ownItem: bool
    description: str | None = None
    webgl: WebGL | None = None
    updated: datetime | None = None


class RecentViewed(BaseModel):
    items: List[Any]
    total: int


class SimilarItems(BaseModel):
    items: List[PublicItem]
    total: int


class OtherSales(BaseModel):
    items: List[PublicItem]
    total: int


class Trend(BaseModel):
    date: date
    value: int
    volume: int


class Trends(BaseModel):
    data: List[Trend]


class Price(BaseModel):
    currency: str
    value: int


class HistoryItem(BaseModel):
    date: str
    wear: str | None = None
    saleId: int
    price: Price


class Rating(BaseModel):
    value: float
    votes: int


class Offers(BaseModel):
    offerCount: int
    highPrice: int
    lowPrice: int
    currency: str


class Version(BaseModel):
    url: str
    price: Price | None = None
    discount: int | None = None
    count: int
    version: str


class RelatedItem(BaseModel):
    url: str
    exterior: str
    type: str | None = None
    quality: str
    price: Any
    discount: Any
    count: int
    default: bool
    versions: List[Version]


class Data(BaseModel):
    item: PublicItem
    recentViewed: RecentViewed
    similarItems: SimilarItems
    otherSales: OtherSales
    recommendedStickers: List[Any]
    trends: Trends
    history: List[HistoryItem]
    rating: Rating
    offers: Offers
    relatedItems: List[RelatedItem]


class ItemResponse(BaseModel):
    requestId: str
    success: bool
    message: str | None = None
    data: Data
