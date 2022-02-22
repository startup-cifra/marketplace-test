from typing import Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: Optional[str] = None


class User(BaseModel):
    login: str
    password: str


class UserDelete(BaseModel):
    login: str


class Customer(BaseModel):
    name: str = Field(None, description='Имя покупателя')


class CutomerNew(Customer):
    password: str = Field(None, description='Пароль покупателя')


class Tag(BaseModel):
    tag_name: str = Field(None, description='Имя тэга')


class Product(BaseModel):
    product_id: int = Field(None, description='ID продукта', gt=0)


class Cart(BaseModel):
    product_id: int = Field(None, description='ID продукта', gt=0)
    product_num: int = Field(1, description='Кол-во продуктов', gt=0)
    customer_name: str = Field(None, description='Имя покупателя')


class CartDelete(BaseModel):
    product_id: int = Field(None, description='ID продукта', gt=0)
    customer_name: str = Field(None, description='Имя покупателя')


class Favourite(BaseModel):
    product_id: int = Field(None, description='ID продукта', gt=0)
    customer_name: str = Field(None, description='Имя покупателя')


class FavouriteOfUser(BaseModel):
    customer_name: str = Field(None, description='Имя покупателя')


class Review(BaseModel):
    product_id: int = Field(None, description='ID продукта', gt=0)
    customer_name: str = Field(None, description='Имя покупателя')
    body: str = Field(None, description='Тело отзыва')
    rating: int = Field(None, description='Рейтинг', ge=1, le=5)
