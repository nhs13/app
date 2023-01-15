import asyncio

from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError

from app.utils.db.connector import engine
from app.utils.db.model import Product


def gen_msg(bool, msg):
    action = "successful"
    if bool != True:
        action = f"un{action}"
    return {"action": action, "msg": msg}


async def get_products(product_id=None):
    """
    list products or get details of one product
    """
    if product_id is None:
        query = select(Product.id)
    else:
        query = select(Product).filter_by(**{"id": product_id})
    async with engine.connect() as conn:
        cursor_result: CursorResult = await conn.execute(query)
        return cursor_result.mappings().all()


async def create_product(args):
    accepted_args = Product.__table__.columns
    args = {k: args[k] for k in args if k in accepted_args}
    stmt = insert(Product).values(**args)
    try:
        async with engine.connect() as conn:
            await conn.execute(stmt)
            await conn.commit()
    except IntegrityError:
        return gen_msg(False, "key already exists")
    return gen_msg(True, "created record")


async def delete_product(product_id):
    try:
        product_id = int(product_id)
    except ValueError:
        return gen_msg(False, "invalid product id")
    query = delete(Product).where(Product.id == product_id)
    async with engine.connect() as conn:
        await conn.execute(query)
        await conn.commit()
        return gen_msg(True, f"deleted product with id {product_id}")


async def update_product(product_id, args):
    query = update(Product).where(Product.id == product_id).values(**args)
    try:
        async with engine.connect() as conn:
            await conn.execute(query)
            await conn.commit()
    except IntegrityError:
        return gen_msg(False, "duplicate name for product")
    return gen_msg(True, "updated record")
