"""
module to start the server of the site.
after installing dependencies, run python server.py
the port will be accessible  on 
"""
import asyncio

from tornado.web import Application

from app.services.auth.handler import get_routes as get_auth_route
from app.services.products.web import get_routes
from app.services.customers.handler import get_routes as get_cust_routes
from tornado.log import enable_pretty_logging

enable_pretty_logging()


async def main():
    app = Application(get_routes() + get_auth_route() + get_cust_routes(), debug=True)
    app.listen(8888)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
