import asyncio

from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError

from app.utils.db.connector import engine
from app.utils.db.model import Order


def gen_msg(bool, msg):
    action = "successful"
    if bool != True:
        action = f"un{action}"
    return {"action": action, "msg": msg}


async def get_orders(order_id=None):
    """
    list orders or get details of one order
    """
    if order_id is None:
        query = select(Order.id)
    else:
        query = select(Order).filter_by(**{"id": order_id})
    async with engine.connect() as conn:
        cursor_result: CursorResult = await conn.execute(query)
        return cursor_result.mappings().all()


async def create_order(args):
    accepted_args = Order.__table__.columns
    args = {k: args[k] for k in args if k in accepted_args}
    stmt = insert(Order).values(**args)
    try:
        async with engine.connect() as conn:
            await conn.execute(stmt)
            await conn.commit()
    except IntegrityError:
        return gen_msg(False, "key already exists")
    return gen_msg(True, "created record")


async def delete_order(order_id):
    try:
        order_id = int(order_id)
    except ValueError:
        return gen_msg(False, "invalid order id")
    query = delete(Order).where(Order.id == order_id)
    async with engine.connect() as conn:
        await conn.execute(query)
        await conn.commit()
        return gen_msg(True, f"deleted order with id {order_id}")


async def update_order(order_id, args):
    query = update(Order).where(Order.id == order_id).values(**args)
    try:
        async with engine.connect() as conn:
            await conn.execute(query)
            await conn.commit()
    except IntegrityError:
        return gen_msg(False, "duplicate name for order")
    return gen_msg(True, "updated record")
