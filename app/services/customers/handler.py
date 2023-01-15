import json
import logging

from tornado.escape import json_decode
from tornado.web import RequestHandler

from app.services.auth.jwt_auth import auth
from app.services.customers.main import create_customer, delete_customer, update_customer,get_customers
import logging

class UsersHandler(RequestHandler):
    """
    class that defines the http calls related to users
    """

    @auth("skip")
    async def get(self, user_id=None):
        logging.info(user_id)
        try:
            if user_id == "":
                res = await get_customers()
            else:
                res = await get_customers(user_id)
        except Exception as e:
            logging.error(e)
            self.set_status(500)
            return self.finish("something went wrong")
        res = [dict(row) for row in res]
        return self.finish(json.dumps(res))

    async def post(self, user_id=None):
        data = json_decode(self.request.body)
        res = await create_customer(data)
        self.finish(json.dumps(res))

    async def patch(self, user_id):
        data = json_decode(self.request.body)
        res = await update_customer(user_id, data)
        self.finish(res)

    async def delete(self, user_id=None):
        res = await delete_customer(user_id)
        self.finish(json.dumps(res))


def get_routes():
    return [
        (r"/users/?(?P<user_id>[^\/]*)", UsersHandler),
    ]
