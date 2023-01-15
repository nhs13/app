import json
import logging

from tornado.escape import json_decode
from tornado.web import RequestHandler

from app.services.auth.jwt_auth import auth
from app.services.products.main import (
    create_product,
    delete_product,
    get_products,
    update_product,
)


class ProductsHandler(RequestHandler):
    """
    class that defines the http calls related to products
    """

    @auth("new role")
    async def get(self, product_id=None):
        try:
            if product_id == "":
                res = await get_products()
            else:
                res = await get_products(int(product_id))
        except Exception as e:
            print(e)
            self.set_status(404)
            return self.finish("product not found")
        res = [dict(row) for row in res]
        self.finish(json.dumps(res))

    async def post(self, product_id=None):
        data = json_decode(self.request.body)
        res = await create_product(data)
        self.finish(json.dumps(res))

    async def patch(self, product_id):
        product_id = int(product_id)
        data = json_decode(self.request.body)
        res = await update_product(product_id, data)
        self.finish(res)

    async def delete(self, product_id=None):
        res = await delete_product(product_id)
        self.finish(json.dumps(res))


def get_routes():
    return [
        (r"/products/?(?P<product_id>[^\/]*)", ProductsHandler),
        # (r"/products", ProductsHandler)
    ]
