from datetime import date
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, RootModel


class Tag(BaseModel):
    name: str | None = None
    name_localized: str | None = None


class GVColorTint(BaseModel):
    W: float | None = None
    X: float | None = None
    Y: float | None = None
    Z: float | None = None


class MaterialProperties(BaseModel):
    g_tColor: str | None = None
    g_tNormal: str | None = None
    g_tMetalness: str | None = None
    g_vColorTint: GVColorTint
    g_tAmbientOcclusion: str | None = None
    g_flPearlescentScale: float | None = None


class Material(BaseModel):
    name: str | None = None
    painted: bool | None = None
    material: MaterialProperties | None = None


class WebGLStatic(BaseModel):
    name: str | None = None
    itemtype: str | None = None
    meshname: str | None = None
    classname: str | None = None
    materials: List[Material] | None = None
    paintname: str | None = None
    paintseed: int | None = None
    paintwear: float | None = None
    offlineurl: str | None = None
    attachments: List[Any] | None = None
    legacymodel: bool | None = None


class WebGLTexture(BaseModel):
    path: str | None = None


class WebGLDynamic(RootModel[Dict[str, WebGLTexture]]):
    root: Dict[str, WebGLTexture]


class WebGL(BaseModel):
    static: WebGLStatic | None = None
    dynamic: WebGLDynamic | None = None


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
    category_localized: str | None = None
    subCategory: str | None = None
    subCategory_localized: str | None = None
    pattern: int | None = None
    finish: int | None = None
    customName: str | None = None
    wear: float | None = None
    link: str | None = None
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
