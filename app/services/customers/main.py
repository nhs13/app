from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError

from app.utils.db.connector import engine
from app.utils.db.model import Auth, Customer


def gen_msg(bool, msg):
    action = "successful"
    if bool != True:
        action = f"un{action}"
    return {"action": action, "msg": msg}


async def get_customers(email=None):
    """
    list customers or get details of one customer
    """
    if email is None:
        query = select(Customer.email)
    else:
        query = select(Customer).filter_by(**{"email": email})
    async with engine.connect() as conn:
        cursor_result: CursorResult = await conn.execute(query)
        return cursor_result.mappings().all()


async def create_customer(args):
    accepted_args = Customer.__table__.columns.keys()
    args = {k: args[k] for k in args if k in accepted_args}
    args['role'] = "customer" if args.get("role",None) is None else args['role']
    try:
        args["first_name"]
        args["last_name"]
        args["email"]
    except KeyError:
        return gen_msg(False, "insufficent params")
    stmt = insert(Customer).values(**args)
    try:
        async with engine.connect() as conn:
            await conn.execute(stmt)
            await conn.commit()
    except IntegrityError:
        return gen_msg(False, "user already exists")
    return gen_msg(True, "created record")


async def delete_customer(customer_id):
    query = delete(Customer).where(Customer.email == customer_id)
    async with engine.connect() as conn:
        await conn.execute(query)
        await conn.commit()
        return gen_msg(True, f"deleted customer with id {customer_id}")


async def update_customer(customer_id, args):
    if "email" in args:
        args.pop("email")
    query = update(Customer).where(Customer.email == customer_id).values(**args)
    try:
        async with engine.connect() as conn:
            await conn.execute(query)
            await conn.commit()
    except IntegrityError:
        return gen_msg(False, "duplicate name for customer")
    return gen_msg(True, "updated record")
