from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional, List
from app.models.product import Product, ProductCategory, ProductList
from app.services.product_service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


def get_product_service() -> ProductService:
    """Dependency для получения сервиса продуктов"""
    return ProductService()


@router.get("/", response_model=ProductList)
async def get_products(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество на странице"),
    category_id: Optional[int] = Query(None, description="ID категории для фильтрации"),
    search: Optional[str] = Query(None, description="Поисковый запрос"),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Получить список продуктов с пагинацией и фильтрацией
    
    Args:
        page: Номер страницы
        per_page: Количество на странице
        category_id: Фильтр по категории
        search: Поиск по названию
        
    Returns:
        ProductList с продуктами
    """
    try:
        return await product_service.get_all_products(
            page=page,
            per_page=per_page,
            category_id=category_id,
            search=search
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения продуктов: {str(e)}"
        )


@router.get("/{slug}", response_model=Product)
async def get_product(
    slug: str,
    product_service: ProductService = Depends(get_product_service)
):
    """
    Получить продукт по slug
    
    Args:
        slug: URL slug продукта
        
    Returns:
        Product
    """
    try:
        product = await product_service.get_product_by_slug(slug)
        
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Продукт '{slug}' не найден"
            )
        
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения продукта: {str(e)}"
        )


@router.get("/categories/", response_model=List[ProductCategory])
async def get_categories(
    product_service: ProductService = Depends(get_product_service)
):
    """
    Получить все категории
    
    Returns:
        List[ProductCategory]
    """
    try:
        return await product_service.get_categories()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения категорий: {str(e)}"
        )


@router.get("/categories/{slug}", response_model=ProductCategory)
async def get_category(
    slug: str,
    product_service: ProductService = Depends(get_product_service)
):
    """
    Получить категорию по slug
    
    Args:
        slug: URL slug категории
        
    Returns:
        ProductCategory
    """
    try:
        category = await product_service.get_category_by_slug(slug)
        
        if not category:
            raise HTTPException(
                status_code=404,
                detail=f"Категория '{slug}' не найдена"
            )
        
        return category
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения категории: {str(e)}"
        )


@router.get("/search/", response_model=List[Product])
async def search_products(
    q: str = Query(..., description="Поисковый запрос"),
    limit: int = Query(10, ge=1, le=50, description="Максимальное количество результатов"),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Поиск продуктов
    
    Args:
        q: Поисковый запрос
        limit: Максимальное количество результатов
        
    Returns:
        List[Product]
    """
    try:
        return await product_service.search_products(query=q, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка поиска продуктов: {str(e)}"
        )
