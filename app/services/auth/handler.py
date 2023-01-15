from json import dumps

from tornado.escape import json_decode, utf8
from tornado.web import RequestHandler

from app.services.auth.main import (
    gen_token,
    register_user,
    update_password,
    validate_user,
)
from app.utils import gen_msg


class AuthHandler(RequestHandler):
    """
    Authentication based on username and password.
    user needs to provide the email and the password.
    """

    async def post(self):
        data = json_decode(self.request.body)
        try:
            secret = data["password"]
            user = data["user"]
        except KeyError:
            self.set_status(402)
            return self.finish(gen_msg(False, "invalid params"))
        is_valid = await validate_user(user, secret)
        if is_valid:
            return self.finish(dumps({"auth": gen_token(user)}))
        else:
            return self.finish(gen_msg(False, "No Access"))

    async def put(self):
        data = json_decode(self.request.body)
        try:
            secret = data["password"]
            user = data["user"]
        except KeyError:
            self.set_status(402)
            return self.finish(gen_msg(False, "invalid params"))
        res = await register_user(user, secret)
        return self.finish(dumps(res))

    async def patch(self):
        data = json_decode(self.request.body)
        try:
            secret = data["password"]
            user = data["user"]
            new_secret = data["new_password"]
        except KeyError:
            self.set_status(402)
            return self.finish(gen_msg(False, "invalid params"))
        is_valid = await validate_user(user, secret)
        if is_valid:
            res = await update_password(user, new_secret)
            return self.finish(dumps(res))
        self.set_status(402)
        return self.finish(gen_msg(False, "sometihng went wrong"))


def get_routes():
    return [
        (r"/auth", AuthHandler),
    ]
