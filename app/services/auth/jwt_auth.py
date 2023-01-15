from typing import Dict

import jwt

from app.utils import gen_msg
import logging

secret_key = "my_secret_key"
options = {
    "verify_signature": True,
    "verify_exp": True,
    "verify_nbf": False,
    "verify_iat": True,
    "verify_aud": False,
}


def gen_token(user, role="standard") -> str:
    return jwt.encode({"user": user, "role": role}, secret_key, algorithm="HS256")


def decode_token(token) -> Dict:
    return jwt.decode(token.encode(), secret_key, algorithms="HS256")


def check_auth(auth):
    print(auth, "auth")
    if auth:
        token = auth
        try:
            data = decode_token(token)
        except Exception as e:
            return False, str(e)
    else:
        return False, "Missing Authorization"
    return True, data


def auth(role=None,skip=True,**kwargs):
    def inner(func,*args,**kwargs):
        async def inner_most(self, *args, **kwargs):
            if skip:
                stat = True
                return  await func(self, *args, **kwargs)
            else:
                auth = self.request.headers.get("Authorization")
                stat, msg = check_auth(auth)
                if msg["role"] not in role:
                    stat = False
                    msg = "UnAuthorized"
            if stat == True:
                return await func(self, *args, **kwargs)
            else:
                self.set_status(401)
                return await self.finish(gen_msg(False, msg))
        return inner_most
    return inner
