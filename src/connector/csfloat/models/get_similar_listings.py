from pydantic import TypeAdapter
from connector.csfloat.models.get_listings import Listing

SimilarListings = TypeAdapter(list[Listing])