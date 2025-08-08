from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ProductCategory(BaseModel):
    """Модель категории продукта"""
    
    id: Optional[int] = None
    name: str = Field(..., description="Название категории")
    slug: str = Field(..., description="URL slug категории")
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Product(BaseModel):
    """Модель продукта"""
    
    id: Optional[int] = None
    name: str = Field(..., description="Название продукта")
    slug: str = Field(..., description="URL slug продукта")
    description: str = Field(..., description="Описание продукта")
    category_id: Optional[int] = None
    category: Optional[ProductCategory] = None
    price: Optional[float] = None
    currency: str = Field(default="RUB")
    images: List[str] = Field(default_factory=list)
    main_image: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ProductList(BaseModel):
    """Список продуктов с пагинацией"""
    
    products: List[Product]
    total: int
    page: int
    per_page: int
    total_pages: int
