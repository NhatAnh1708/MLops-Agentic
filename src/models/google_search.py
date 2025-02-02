from pydantic import BaseModel, Field
from typing import List, Optional


class ShoppingItem(BaseModel):
    title: str
    source: str
    price: str
    link: str
    delivery: Optional[str]
    rating: Optional[float]
    ratingCount: Optional[int]


class ShoppingSearchResult(BaseModel):
    items: List[ShoppingItem] = Field(..., description="List of shopping items found")
    analysis: str = Field(..., description="AI analysis of the shopping results")


class ProductAnalysis(BaseModel):
    price_range: str = Field(..., description="Price range of the products")
    best_value: str = Field(..., description="Best value for money option")
    popular_stores: List[str] = Field(
        ..., description="Most popular stores selling the product"
    )
    recommendation: str = Field(..., description="AI recommendation based on the data")
