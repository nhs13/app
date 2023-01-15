import asyncio

from app.services.auth.main import (
    fetch_user_hash,
    register_user,
    update_password,
    validate_user,
)
from app.services.customers.main import create_customer, get_customers
from app.services.products.main import get_products

args = {"first_name": "A", "last_name": "B", "email": "a@b.com"}
#


async def main():
    a = await create_customer(args)
    print(a)
    b = await register_user("a@b.com", "pass")
    print(b)
    c = await fetch_user_hash("a@b.com")
    print(c)
    d = await validate_user("a@b.com", "pass")
    print(d)
    e = await update_password("a@b.com", "pass")
    print(e)
    a = await get_customers()
    print(a, "gc")


print(asyncio.run(main()))
