import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.product import Product, ProductCategory, ProductList
from config.settings import get_settings

logger = logging.getLogger(__name__)


class ProductService:
    """Сервис для работы с продуктами"""
    
    def __init__(self):
        self.settings = get_settings()
        # Временные данные продуктов (в будущем будет база данных)
        self._products = self._initialize_products()
        self._categories = self._initialize_categories()
    
    def _initialize_categories(self) -> List[ProductCategory]:
        """Инициализация категорий"""
        return [
            ProductCategory(
                id=1,
                name="Acne Studios",
                slug="acne",
                description="Премиальные футболки от Acne Studios",
                image_url="img/tshirt1.png"
            ),
            ProductCategory(
                id=2,
                name="HP Health",
                slug="hphealth",
                description="HP Health HP T-Shirt",
                image_url="img/tshirt2.png"
            ),
            ProductCategory(
                id=3,
                name="Zip Hoodie",
                slug="zip",
                description="Zip Hoodie Army",
                image_url="img/zip1.png"
            ),
            ProductCategory(
                id=4,
                name="Poizon",
                slug="poizon",
                description="Poizon - платформа для покупки и продажи",
                image_url="img/tshirt1.png"
            )
        ]
    
    def _initialize_products(self) -> List[Product]:
        """Инициализация продуктов"""
        return [
            Product(
                id=1,
                name="Acne Studios T-Shirt",
                slug="acne-studios-tshirt",
                description="Премиальные футболки от Acne Studios",
                category_id=1,
                price=1800.0,
                images=["img/tshirt1.png", "img/tshirt1.webp", "img/tshirt1_2.jpeg", "img/tshirt1_3.jpeg"],
                main_image="img/tshirt1.png"
            ),
            Product(
                id=2,
                name="HP Health HP T-Shirt",
                slug="hp-health-tshirt",
                description="HP Health HP T-Shirt",
                category_id=2,
                price=1200.0,
                images=["img/tshirt2.png", "img/tshirt2.webp", "img/tshirt2_2.jpeg", "img/tshirt2_3.jpeg"],
                main_image="img/tshirt2.png"
            ),
            Product(
                id=3,
                name="Zip Hoodie Army",
                slug="zip-hoodie-army",
                description="Zip Hoodie Army",
                category_id=3,
                price=4800.0,
                images=["img/zip1.png", "img/zip1.webp", "img/zip1_2.jpeg", "img/zip1_3.jpeg", "img/zip1_4.jpeg"],
                main_image="img/zip1.png"
            )
        ]
    
    async def get_all_products(
        self, 
        page: int = 1, 
        per_page: int = 10,
        category_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> ProductList:
        """
        Получить все продукты с пагинацией
        
        Args:
            page: Номер страницы
            per_page: Количество на странице
            category_id: Фильтр по категории
            search: Поиск по названию
            
        Returns:
            ProductList с продуктами
        """
        try:
            # Фильтрация
            filtered_products = self._products.copy()
            
            if category_id:
                filtered_products = [p for p in filtered_products if p.category_id == category_id]
            
            if search:
                search_lower = search.lower()
                filtered_products = [
                    p for p in filtered_products 
                    if search_lower in p.name.lower() or search_lower in p.description.lower()
                ]
            
            # Пагинация
            total = len(filtered_products)
            total_pages = (total + per_page - 1) // per_page
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            
            products = filtered_products[start_idx:end_idx]
            
            # Добавляем информацию о категориях
            for product in products:
                product.category = next(
                    (cat for cat in self._categories if cat.id == product.category_id),
                    None
                )
            
            return ProductList(
                products=products,
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages
            )
            
        except Exception as e:
            logger.error(f"Ошибка получения продуктов: {str(e)}")
            return ProductList(
                products=[],
                total=0,
                page=page,
                per_page=per_page,
                total_pages=0
            )
    
    async def get_product_by_slug(self, slug: str) -> Optional[Product]:
        """
        Получить продукт по slug
        
        Args:
            slug: URL slug продукта
            
        Returns:
            Product или None
        """
        try:
            product = next(
                (p for p in self._products if p.slug == slug),
                None
            )
            
            if product:
                product.category = next(
                    (cat for cat in self._categories if cat.id == product.category_id),
                    None
                )
            
            return product
            
        except Exception as e:
            logger.error(f"Ошибка получения продукта {slug}: {str(e)}")
            return None
    
    async def get_categories(self) -> List[ProductCategory]:
        """
        Получить все категории
        
        Returns:
            List[ProductCategory]
        """
        try:
            return self._categories
        except Exception as e:
            logger.error(f"Ошибка получения категорий: {str(e)}")
            return []
    
    async def get_category_by_slug(self, slug: str) -> Optional[ProductCategory]:
        """
        Получить категорию по slug
        
        Args:
            slug: URL slug категории
            
        Returns:
            ProductCategory или None
        """
        try:
            return next(
                (cat for cat in self._categories if cat.slug == slug),
                None
            )
        except Exception as e:
            logger.error(f"Ошибка получения категории {slug}: {str(e)}")
            return None
    
    async def search_products(self, query: str, limit: int = 10) -> List[Product]:
        """
        Поиск продуктов
        
        Args:
            query: Поисковый запрос
            limit: Максимальное количество результатов
            
        Returns:
            List[Product]
        """
        try:
            query_lower = query.lower()
            results = []
            
            for product in self._products:
                if (query_lower in product.name.lower() or 
                    query_lower in product.description.lower()):
                    results.append(product)
                    if len(results) >= limit:
                        break
            
            return results
            
        except Exception as e:
            logger.error(f"Ошибка поиска продуктов: {str(e)}")
            return []
