# coding: utf-8
from sqlalchemy import (
    JSON,
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata
Base.metadata.schema = "app"


class Addres(Base):
    __tablename__ = "address"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text("nextval('address_id_seq'::regclass)"),
    )
    line_1 = Column(String)
    line_2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    pincode = Column(String)
    user_id = Column(String)


class Auth(Base):
    __tablename__ = "auth"

    email = Column(String, primary_key=True)
    pass_hash = Column(String)


class Cart(Base):
    __tablename__ = "cart"

    user_id = Column(String, primary_key=True)
    products = Column(JSON)


class OrderLineItem(Base):
    __tablename__ = "order_line_items"

    line_item_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('order_line_items_line_item_id_seq'::regclass)"),
    )
    order_id = Column(String)
    cost = Column(String)
    quantity = Column(String)
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(String)


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text("nextval('orders_id_seq'::regclass)"),
    )
    order_price = Column(BigInteger)
    billed_price = Column(BigInteger)
    customer_paid = Column(BigInteger)
    status = Column(String)
    user_email = Column(String)
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Price(Base):
    __tablename__ = "prices"

    product_id = Column(BigInteger, primary_key=True)
    price_per_unit = Column(BigInteger)
    discounted_price = Column(BigInteger)


class Procurement(Base):
    __tablename__ = "procurement"

    product_id = Column(BigInteger, primary_key=True, nullable=False)
    quantity = Column(BigInteger, server_default=text("0"))
    cost = Column(BigInteger, server_default=text("0"))
    shop_name = Column(String, primary_key=True, nullable=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text("nextval('products_id_seq'::regclass)"),
    )
    name = Column(String, nullable=False, unique=True)
    type = Column(String)
    classification = Column(String)
    details = Column(JSON)


class Wishlist(Base):
    __tablename__ = "wishlist"

    user_id = Column(String, primary_key=True)
    products = Column(JSON)


class Customer(Base):
    __tablename__ = "customers"

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, primary_key=True)
    phone = Column(String)
    default_address_id = Column(ForeignKey("address.id"))
    role = Column(String)

    default_address = relationship("Addres")
