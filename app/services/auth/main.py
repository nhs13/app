from passlib.exc import InvalidHashError
from passlib.hash import pbkdf2_sha256
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from app.services.auth.jwt_auth import decode_token, gen_token
from app.utils.db.connector import engine
from app.utils.db.model import Auth

"""
dont change the salt !!! never change this salt
"""
__salt = "secret_salt".encode()
hasher = pbkdf2_sha256.using(salt=__salt)


def gen_msg(bool, msg):
    action = "successful"
    if bool != True:
        action = f"un{action}"
    return {"action": action, "msg": msg}


async def validate_user(user, secret):
    computed = hasher.hash(secret)
    stored_hash = await fetch_user_hash(user)
    try:
        return hasher.verify(secret, stored_hash)
    except TypeError:
        return False


async def fetch_user_hash(email):
    query = select(Auth.pass_hash).filter_by(email=email)
    async with engine.connect() as conn:
        cursor_result = await conn.execute(query)
        try:
            return cursor_result.mappings().all()[0]["pass_hash"]
        except IndexError:
            return False


def hash_password(password):
    return hasher.hash(password)


async def register_user(email, password):
    password = hash_password(password)
    query = insert(Auth).values(email=email, pass_hash=password)
    try:
        async with engine.connect() as conn:
            await conn.execute(query)
            await conn.commit()
        return gen_msg(True, "user registered successfully")
    except IntegrityError:
        return gen_msg(False, "account already exists")


async def update_password(email, password):
    password = hash_password(password)
    query = update(Auth).where(Auth.email == email).values(pass_hash=password)
    async with engine.connect() as conn:
        await conn.execute(query)
        await conn.commit()
    return gen_msg(True, f"updated password for {email}")


async def remove_auth(email):
    query = delete(Auth).where(Auth.email == email)
    async with engine.connect() as conn:
        await conn.execute(query)
        await conn.commit()
    return gen_msg(True, f"deleted creds for {email}")
