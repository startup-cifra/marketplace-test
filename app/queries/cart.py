from asyncpg import Record
from app.db.db import DB
from app.exceptions import BadRequest, CustomerNotFoundException
from app.queries.customer import get_customer_id
from app.settings import ITEMS_PER_PAGE


async def add_product_to_cart(customer_name: str, product_id: int, product_num: int) -> None:
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = '''  INSERT INTO cart_product(customer_id, product_id, product_num)
               VALUES ($1,$2,$3);'''
    if not await DB.con.execute(sql, customer_id, product_id, product_num):
        raise BadRequest('Продукт уже добавлен в корзину')


async def update_product_in_cart(customer_name: str, product_id: int, product_num: int) -> None:
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = '''  UPDATE cart_product
               SET product_num = $1
               WHERE customer_id = $2 AND product_id = $3'''
    if not await DB.con.execute(sql, customer_id, product_id, product_num):
        raise BadRequest('Такого продукта не существует')


async def delete_product_from_cart(customer_name: str, product_id: int) -> None:
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = '''  DELETE FROM cart_product
               WHERE product_id = $1 AND customer_id = $2;'''
    await DB.con.execute(sql, product_id, customer_id)
    


async def get_cart_products(customer_name: str, previous_id: int) -> list[Record]:
    customer_id = await get_customer_id(customer_name)
    if not customer_id:
        raise CustomerNotFoundException
    sql = """  SELECT p.id AS product_id,
                      p.name,
                      p.price,
                      p.url,
                      CASE
                        WHEN favourite.product_id = p.id THEN 'Yes'
                        ELSE 'No'
                      END AS Love,
                      cart_product.product_num,
                      cart_product.id AS previous_id
               FROM cart_product
               JOIN product p ON p.id = cart_product.product_id
               AND customer_id = $1
               LEFT JOIN favourite ON favourite.customer_id = $1
                AND favourite.product_id = p.id
               WHERE  cart_product.id > $2
               LIMIT $3;"""
    return await DB.con.fetch(sql, customer_id, previous_id, ITEMS_PER_PAGE)
